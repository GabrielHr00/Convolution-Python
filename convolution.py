import numpy as np 

def periodical_convolution(w, w_cut, x_size):
    # circular convolution
    # cut the convoled signal with length the given period -> x_size
    # and then add the rest of the values to the corresponding indexes, 
    # where if the index is out of bound beginn from 0
    start_index = len(w_cut)
    counter = 0
    i = start_index
    for x_size in range(len(w)):
        if counter == len(w_cut):
            counter = 0
        if start_index >= len(w):
            break;
        w_cut[counter] += w[start_index]
        counter += 1
        start_index += 1
    return w_cut

def construct_overlapping(w, x, h, valid_size, w_size):
    # when overlapping the vector should have length of max(x_size, h_size) - min(x_size,h_size) + 1, which is valid_size
    # then take the values from the convolved signal from the middle considering the even or odd length of the signal
    w_new = np.zeros((1,valid_size), dtype='int')
    if w_size % 2 == 0:
        start = round(w_size/2 - valid_size/2)
        for i in range(0, valid_size):
            w_new[0,i] = w[start]
            start += 1
    else:
        start = int(w_size/2 - valid_size/2)
        for i in range(0, valid_size):
            w_new[0,i] = w[start]
            start += 1
    return w_new[0]
    
        
def convolve_two_signals(w_size, x, h):
    # two for loops, the first and second goes from 0 to x_size + h_size - 1
    # and multiply the values on the current index and then sum it to get the convolution on a given index
    
    w = np.zeros((1,w_size), dtype='int')
    for i in range(0, w_size):
        sum = 0
        for j in range(0, w_size):
            sum += x[j] * h[i - j]
            if i == j:
                break;
        w[0,i] = sum 
    return w[0]
    

def con1(x, h, overlap, periodic):
    x_size = len(x)
    h_size = len(h)
    period = x_size
    valid_size = max(x_size, h_size) - min(x_size,h_size) + 1
    w_size = x_size + h_size - 1 
    
    #if the x or h vector are empty, print an error message
    
    if x_size == 0 or h_size == 0:
        print("The signal cannot be empty")
    
    # fill with zeros the two signals until they have length of x_size + h_size - 1,
    # so we dont hove to check in the for loops and just multiply 
    
    for i in range(w_size - x_size):
            x.append(0)
    for i in range(w_size - h_size):
            h.append(0)
    
    # check for periodicity and overlapping
    if periodic == False and overlap == False:
        w = convolve_two_signals(w_size, x, h)       
    elif periodic == True and overlap == False:
        w = convolve_two_signals(w_size, x, h)
        w_cut = convolve_two_signals(period, x, h)
        w = periodical_convolution(w, w_cut, x_size)
    elif periodic == False and overlap == True:
        w = convolve_two_signals(w_size, x, h)
        w = construct_overlapping(w, x, h, valid_size, w_size)
    elif periodic == True and overlap == True: 
        # this case is a little bit tricky, (both true)
        # first we calculate the convolution
        # second we take the overlapping parts
        # third copy the first elements from the overlapped convolled signal -> period
        # and then do the periodic convolution with the overlapped vector and the trimmed "new" signal
        w = convolve_two_signals(w_size, x, h)
        w = construct_overlapping(w, x, h, valid_size, w_size)
        w_cut = w[:period]
        w = periodical_convolution(w, w_cut, x_size)
    return w
     
x = [1,2]
y = [3,1,5,2,4,1]
S = con1(x, y, overlap=True, periodic=True)
S



# Should do the same as the following numpy function
import numpy as np

c = [1,2,3]
y = [3,1,5,67,2,9,56]
s = np.convolve(c, y, mode='valid')
s

#The output of conv1(x,h,overlap=True,periodic=False) should be equal to
# numpy.convolve(x,h,mode="valid") and the output of conv1(x,h,overlap=False,periodic=False) should be equal to numpy.convolve(x,h,mode="full")