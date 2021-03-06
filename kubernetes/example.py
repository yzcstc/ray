from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import Counter
import socket
import sys
import time
import ray

if __name__ == "__main__":
    ray.init(redis_address="{}:6379".format(socket.gethostbyname("ray-head")))

    # Wait for all 4 nodes to join the cluster.
    while True:
        num_nodes = len(ray.global_state.client_table())
        if num_nodes < 4:
            print("{} nodes have joined so far. Waiting for more."
                  .format(num_nodes))
            sys.stdout.flush()
            time.sleep(1)
        else:
            break

    @ray.remote
    def f(x):
        time.sleep(0.01)
        return x + (ray.services.get_node_ip_address(), )

    # Check that objects can be transferred from each node to each other node.
    for i in range(100):
        print("Iteration {}".format(i))
        sys.stdout.flush()
        print(Counter(ray.get([f.remote(f.remote(())) for _ in range(10000)])))
        sys.stdout.flush()

    print("Success!")
    sys.stdout.flush()
