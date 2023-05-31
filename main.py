from matplotlib import pyplot as plt

from  Field import Field

def plot():
    text_file = open("sarsav3.txt", "r")
    sarsa = text_file.readlines()[0].split(' ')
    sarsa.pop()
    sarsa = [int(item) for item in sarsa]
    text_file = open("sarsa_expectedv3.txt", "r")
    exp_sarsa = text_file.readlines()[0].split(' ')
    exp_sarsa.pop()
    exp_sarsa = [int(item) for item in exp_sarsa]

    text_file = open("q_learningv3.txt", "r")

    qlearning = text_file.readlines()[0].split(' ')
    qlearning.pop()
    qlearning = [int(item) for item in qlearning]

    ext_file = open("qq_learningv3.txt", "r")
   # print(ext_file.readlines()[0])
    qqlearning = ext_file.readlines()[0].split(' ')
    qqlearning.pop()
    qqlearning = [int(item) for item in qqlearning]
    x = [i for i in range(300)]
    plt.plot(x, sarsa, label = "sarsa")
    plt.plot(x, qlearning, label = "qlearning")
    plt.plot(x, qqlearning, label = "qqlearning")
    plt.plot(x, exp_sarsa, label = "expected_sarsa")

    plt.legend()
    plt.grid(True)
    plt.show()


def test(x):
    #print("sarsa")
    #x.Sarsa()
    #print("qlearning")
    #x.Q_learning()
    print("qq_learning")
    x.QQ_learning()
    print("expected sarsa")
    x.expected_Sarsa()

if __name__ == '__main__':
    x = Field()
    x.start()
    #for  i in range(1000):
       # x.visualisation()
    x.Q_learning()


