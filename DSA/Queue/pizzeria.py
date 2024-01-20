from Queue import Queue
import time
import threading

orderQueue = Queue()


def placeOrder(orderList):
    for order in orderList:
        print('Initializing new order procedure')
        time.sleep(0.5)
        orderQueue.enqueue(order)
        print(f"Order for {order} placed successfully")


def serveOrder():
    while orderQueue.getSize() != 0:
        print('Initializing order serve procedure')
        print(orderQueue.container)
        time.sleep(2)
        print(f"Order for {orderQueue.dequeue()} served successfully")


orderList = ['pizza', 'samosa', 'pepperoni', 'pasta', 'biryani', 'burger']
orderThread = threading.Thread(target=placeOrder, args=(orderList,))
completionThread = threading.Thread(target=serveOrder)


orderThread.start()
time.sleep(1)
completionThread.start()
