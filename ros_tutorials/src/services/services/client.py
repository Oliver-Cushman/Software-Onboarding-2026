# Assignment: Create a ROS 2 Service That Generates a Random Number
# In this exercise, you will build a client node that requests a random integer
# from a service server. The client sends a minimum and maximum value, and the
# service responds with a generated number within that range.
#
# The exercise introduces the basic ROS 2 service client pattern:
# - create a custom node class that inherits from rclpy.node.Node
# - initialize the node with a unique name, such as "random_number_client"
# - create a client with self.create_client(...)
# - define a request object with the required fields
# - call the service and wait for a response
# - log or print the returned result
#
# This file is the client half of the exercise. It sends a request to the server
# and prints the generated random value. Together, these two nodes demonstrate
# how ROS 2 services provide synchronous request/response communication.

import rclpy
from rclpy.node import Node
from interfaces.srv import RandomNumber 

# Service design:
#   Request: min_value, max_value
#   Response: random_number
# 
# Here, import RandomNumber from the interfaces.srv module
# RandomNumber is the custom Service type.

# ROS 2 boilerplate pattern:
# 1. Import rclpy and the base Node class.
# 2. Create a custom node class that inherits from Node.
# 3. In __init__, call super().__init__("node_name") to register the node.
# 4. Add services, publishers, subscribers, timers, and other ROS interfaces in __init__.
# 5. In main(), initialize rclpy, create the node, then spin it.
#    Finally destroy the node and shutdown ROS. NOTE: Change this
#
# This pattern is the standard starting point for most ROS 2 Python nodes.


class ServiceClient(Node):
    def __init__(self):
        super().__init__('service_client')

        self.client = self.create_client(RandomNumber, 'generate_random_number')

        while self.client.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info('Service not available, waiting again...')

        self.get_logger().info('Service is available!')

        # TODO: Create a client for the random-number service
        # TODO: Wait for the service to be available

        # create_client:
        #   Creates a service client used to call a ROS service.
        #   Usage: self.create_client(ServiceType, 'service_name')
        #   - ServiceType: the ROS service class you defined in an .srv file
        #   - 'service_name': name of the service to call
        #   Typical use: request a computation, configuration, or value from a server.
        #
        # self.get_logger():
        #   Returns the node's ROS logger, used to print request/response details.
        #   Usage: self.get_logger().info('message')

    # Create a method that sends the service request.
    def send_request(self):
        # TODO: Create a request containing min and max values
        # TODO: Call the service

        # NOTE: Add call_async instructions
        
        req = RandomNumber.Request()
        req.min_value = 1
        req.max_value = 100
        return self.client.call_async(req)

def main():
    rclpy.init()
    node = ServiceClient()
    
    future = node.send_request()
    rclpy.spin_until_future_complete(node, future)

    try:
        response = future.result()
        node.get_logger().info(
            f'Generated number: {response.random_number}'
        )
    except Exception as error:
        node.get_logger().error(f'Service call failed: {error}')

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    