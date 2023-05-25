import rospy
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
import cv2


class CameraSubscriber:
    def __init__(self):
        self.bridge = CvBridge()

        self.camera1_pub = rospy.Publisher('/camera1/image_raw', Image, queue_size=10)
        self.camera2_pub = rospy.Publisher('/camera2/image_raw', Image, queue_size=10)
        self.camera3_pub = rospy.Publisher('/camera3/image_raw', Image, queue_size=10)
        self.camera4_pub = rospy.Publisher('/camera4/image_raw', Image, queue_size=10)

        self.sub = rospy.Subscriber('/ImageJpeg/compressed/Image', Image, self.callback)
        self.camera_info_sub = rospy.Subscriber('/Image/compressed/camera_info', CameraInfo, self.camera_info_callback)

        self.camera_names = ['Camera_Front', 'Camera_Right', 'Camera_Back', 'Camera_Left']
        self.current_camera = None

    def camera_info_callback(self, msg):
        self.current_camera = msg.camera_name

    def callback(self, msg):
        if self.current_camera is not None:

            try:
                cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            except Exception as e:
                print(e)

            if self.current_camera == self.camera_names[0]:
                self.camera1_pub.publish(msg)
            elif self.current_camera == self.camera_names[1]:
                self.camera2_pub.publish(msg)
            elif self.current_camera == self.camera_names[2]:
                self.camera3_pub.publish(msg)
            elif self.current_camera == self.camera_names[3]:
                self.camera4_pub.publish(msg)


if __name__ == '__main__':
    rospy.init_node('camera_subscriber', anonymous=True)
    camera_subscriber = CameraSubscriber()
    rospy.spin()
