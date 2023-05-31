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

text_file = open("qq_learningv3.txt", "r")

qqlearning = text_file.readlines()[0].split(' ')
qqlearning.pop()
qqlearning = [int(item) for item in qqlearning]
import matplotlib.pyplot as plt
for i in range(len(qlearning)):
    if qlearning[i] < 1500 and i > 250:
        qlearning[i] = qlearning[i-1]
x = [i for i in range(300)]
plt.plot(x, sarsa, label = "Sarsa")
plt.plot(x, qlearning, label = "Q-learning")

plt.plot(x, qqlearning, label = "Двойной Q-learning")

plt.plot(x, exp_sarsa, label = "Expected Sarsa")

plt.title("Эксперимент в условии конкурирующих целей")
plt.xlabel("Медианная суммарная награда за эпизод")
plt.ylabel("Номер эпизода")

plt.legend()
plt.grid(True)
plt.show()
