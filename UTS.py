
#!/usr/bin/env python3

import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class GerakCmdVel(Node):

    def __init__(self):
        super().__init__('gerak_cmd_vel')

        self.publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.get_logger().info('Node gerak_cmd_vel aktif.')

        self.urutan_gerak = [
            (0, -1, 2),       # 1
            (1,  0, 8),       # 2
            (0,  1, 2),       # 3
            (1,  0, 8),       # 4
            (0, -1, 2),       # 5
            (1,  0, 3),       # 6
            (0,  1, 2),       # 7
            (1,  0, 4.5),     # 8
            (0,  1, 2),       # 9
            (1,  0, 8),       # 10
            (0, -1, 2),       # 11
            (1,  0, 14),      # 12
            (0, -1, 2),       # 13
            (1,  0, 17),      # 14
            (1, -0.25, 16),   # 15
            (1,  0, 5),       # 16
            (0,  1, 2),       # 17
            (1,  0, 3),       # 18
            (0,  1, 2),       # 19
            (1,  0, 8),      # 20
            (0, -1, 2),       # 21
            (1,  0, 8),       # 22
            (0,  1, 2),       # 23
            (1,  0, 3),       # 24
            (0, -1, 2),       # 25
            (1,  0, 4),       # 26
            (0, -1, 2),       # 27
            (1,  0, 9),       # 28
        ]

    def kirim_perintah(self, vy, w, durasi):
        msg = Twist()

        msg.linear.x = float(vy)
        msg.linear.y = 0.0
        msg.angular.z = float(w)

        periode = 0.05  # 20 Hz
        mulai = time.monotonic()

        try:
            while rclpy.ok():
                elapsed = time.monotonic() - mulai

                if elapsed >= durasi:
                    break

                self.publisher.publish(msg)
                time.sleep(min(periode, durasi - elapsed))

        finally:
            self.berhenti()

    def berhenti(self):
        msg = Twist()

        for _ in range(5):
            self.publisher.publish(msg)
            time.sleep(0.05)

    def jalankan_urutan(self):
        total = len(self.urutan_gerak)

        for nomor, (vy, w, durasi) in enumerate(
            self.urutan_gerak, start=1
        ):
            if not rclpy.ok():
                break

            self.get_logger().info(
                f'Gerakan {nomor}/{total} | '
                f'Vy={vy} m/s | '
                f'w={w} rad/s | '
                f't={durasi} s'
            )

            self.kirim_perintah(vy, w, durasi)

        self.berhenti()
        self.get_logger().info('Semua urutan gerakan selesai.')


def main(args=None):
    rclpy.init(args=args)
    node = GerakCmdVel()

    try:
        input('Tekan Enter untuk memulai 28 urutan gerakan...')
        node.jalankan_urutan()

    except KeyboardInterrupt:
        print('\nGerakan dihentikan oleh pengguna.')

    finally:
        node.berhenti()
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()

