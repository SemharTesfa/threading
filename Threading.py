from sklearn.linear_model import LinearRegression
from pandas import DataFrame
import matplotlib.pyplot as plt;plt.rcdefaults()
import threading
from DatabasePy import Database


class ThreadingElements(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.data = {}
        self.D = Database('SQLite_Python.db', 'Database')
        self.lock = threading.Lock()

    def run(self, element):
        print(f'{self.getName()} has started!')
        self.data = self.D.temp(element, self.lock)
        self.create_linear_regression()
        print(f'{self.getName()} has finished!')

    def create_linear_regression(self):
        data = self.data
        keys = data.keys()
        values = [data[key] for key in keys]

        X = DataFrame(keys).values.reshape(-1, 1)
        Y = DataFrame(values).values.reshape(-1, 1)

        linear_regressor = LinearRegression()  # create object for the class
        linear_regressor.fit(X, Y)  # perform linear regression
        Y_pred = linear_regressor.predict(X)  # make predictions
        plt.scatter(X, Y)
        plt.plot(X, Y_pred, color='red')
        plt.xlabel('Year')
        plt.ylabel('Global Radiative Forcing (W m-2)')
        plt.title('ANNUAL GREENHOUSE GAS INDEX')
        ax = plt.gca()
        ax.set_xlim([1987,2020])


if __name__ == '__main__':
    threads = []
    elementList = ['CO2', 'CH4', 'N2O', 'CFC12', 'CFC11', 'minor']

    for i in elementList:
        t = ThreadingElements()
        x = threading.Thread(target=t.run(i))
        threads.append(x)
        x.start()
        plt.show()

    for thread in threads:
        thread.join()








"""
class ThreadingElements(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.data = {}
        self.D = Database('SQLite_Python.db', 'Database')
        self.lock = threading.Lock()

    def run(self, element):
        print(f'{self.getName()} has started!')
        self.data = self.D.temp(element, self.lock)
        self.create_linear_regression()
        print(f'{self.getName()} has finished!')

    def create_linear_regression(self):
        data = self.data
        keys = data.keys()
        values = [data[key] for key in keys]

        X = DataFrame(keys).values.reshape(-1, 1)
        Y = DataFrame(values).values.reshape(-1, 1)

        linear_regressor = LinearRegression()  # create object for the class
        linear_regressor.fit(X, Y)  # perform linear regression
        Y_pred = linear_regressor.predict(X)  # make predictions
        plt.scatter(X, Y)
        plt.plot(X, Y_pred, color='red')
        plt.xlabel('Year')
        plt.ylabel('Global Radiative Forcing (W m-2)')
        plt.title('ANNUAL GREENHOUSE GAS INDEX')
        ax = plt.gca()
        ax.set_xlim([1987,2020])


if __name__ == '__main__':
    threads = []
    elementList = ['CO2', 'CH4', 'N2O', 'CFC12', 'CFC11', 'minor']

    for i in elementList:
        t = ThreadingElements()
        x = threading.Thread(target=t.run(i))
        threads.append(x)
        x.start()
        plt.show()

    for thread in threads:
        thread.join()

"""
