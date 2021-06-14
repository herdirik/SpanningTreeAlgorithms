import flood_st
import tarry_st
import matplotlib.pyplot as plt

f_messageCounts = [0]*4
t_messageCounts = [0]*4
f_runtimes = [0]*4
t_runtimes = [0]*4
f_diameters = [0]*4
t_diameters = [0]*4

x = [20,40,60,80]


print("Flood_ST icin 20 nodes")
f_messageCounts[0], f_runtimes[0], f_diameters[0] = flood_st.test(20)
print('\n')
print("Flood_ST icin 40 nodes")
f_messageCounts[1], f_runtimes[1], f_diameters[1] = flood_st.test(40)
print('\n')
print("Flood_ST icin  60 nodes")
f_messageCounts[2], f_runtimes[2], f_diameters[2] = flood_st.test(60)
print('\n')
print("Flood_ST icin 80 nodes")
f_messageCounts[3], f_runtimes[3], f_diameters[3] = flood_st.test(80)
print('\n')


print("Tarry_ST icin  20 nodes")
t_messageCounts[0], t_runtimes[0], t_diameters[0] = tarry_st.test(20)
print('\n')
print("Tarry_ST icin  40 nodes")
t_messageCounts[1], t_runtimes[1], t_diameters[1] = tarry_st.test(40)
print('\n')
print("Tarry_ST icin  60 nodes")
t_messageCounts[2], t_runtimes[2], t_diameters[2] = tarry_st.test(60)
print('\n')
print("Tarry_ST icin 80 nodes")
t_messageCounts[3], t_runtimes[3], t_diameters[3] = tarry_st.test(80)
print('\n')

# Flood_ST algoritması için 20, 60 ve 80 node içeren graphlara gore messageCount, runtime ve diameter değerleri.
print ("Flood_ST için 20, 40, 60 ve 80 node iceren graphlara gore message count değerleri")
print (f_messageCounts)
print ("Flood_ST için 20, 40, 60 ve 80 node iceren graphlara gore runtime değerleri")
print(f_runtimes)
print ("Flood_ST için 20, 40, 60 ve 80 node iceren graphlara gore diameter değerleri")
print(f_diameters)
print ("\n ")
# Tarry_ST  algoritması için 20, 60 ve 80 node içeren graphlara gore messageCount, runtime ve diameter değerleri.
print ("Tarry_ST için 20, 40, 60 ve 80 node iceren graphlara gore message count değerleri")
print(t_messageCounts)
print ("Tarry_ST için 20, 40, 60 ve 80 node iceren graphlara gore runtime değerleri")
print(t_runtimes)
print ("Tarry_ST için 20, 40, 60 ve 80 node iceren graphlara gore diameter değerleri")
print(t_diameters)

#grafikleri cizdirme 

plt.figure(1)
plt.subplot(111)
plt.plot(x,f_messageCounts, label = "Flood ST Algorithm",linestyle='--', marker='o')
plt.plot(x,t_messageCounts, label = "Tarry ST Algorithm",linestyle='--', marker='o')
plt.legend()
plt.title('Message Counts')
plt.figure(2)
plt.subplot(111)
plt.plot(x,f_runtimes, label = "Flood ST Algorithm",linestyle='--', marker='o')
plt.plot(x,t_runtimes, label = "Tarry ST Algorithm",linestyle='--', marker='o')
plt.legend()
plt.title('Runtimes')
plt.figure(3)
plt.subplot(111)
plt.plot(x,f_diameters, label = "Flood ST Algorithm",linestyle='--', marker='o')
plt.plot(x,t_diameters, label = "Tarry ST Algorithm",linestyle='--', marker='o')
plt.legend()
plt.title('Diameters')
plt.show()