from csv import reader
from sys import exit
from math import sqrt
from operator import itemgetter
import pickle


def load_data_set(filename):
    try:
        with open(filename, newline='') as iris:
            return list(reader(iris, delimiter=','))
    except FileNotFoundError as e:
        raise e


def convert_to_float(data_set, mode):
    new_set = []

    try:
        if mode == 'training':
            for data in data_set:
                new_set.append([float(x) for x in data[:len(data)-1]] + [data[len(data)-1]])

        elif mode == 'test':
            for data in data_set:
                print(data)
                new_set.append([float(x) for x in data])

        elif mode == 'predict':
            for data in data_set:
                print(data)
                new_set.append([float(x) for x in data])

        else:
            print('Invalid mode, program will exit.')
            exit()

        return new_set

    except ValueError as v:
        print(v)
        print('Invalid data set format, program will exit.')
        exit()


def get_classes(training_set):
    return list(set([c[-1] for c in training_set]))
    

def find_neighbors(distances, k):
    return distances[0:k]


def find_response(neighbors, classes):
    votes = [0] * len(classes)

    for instance in neighbors:
        for ctr, c in enumerate(classes):
            if instance[-2] == c:
                votes[ctr] += 1

    return max(enumerate(votes), key=itemgetter(1))


def knn(training_set, test_set, k):
    global CROP_VALUE, ARRAY_PREDICTION
    predicted_result = ""
    distances = []
    dist = 0
    limit = len(training_set[0]) - 1
    print("HAI")

    # generate response classes from training data
    classes = get_classes(training_set)
    print("hello")
    
    try:
        print("hooo")
        for test_instance in test_set:
            print("test set", test_instance)
            for row in training_set:
                for x, y in zip(row[:limit], test_instance):
                    dist += (x-y) * (x-y)
                distances.append(row + [sqrt(dist)])
                dist = 0

            distances.sort(key=itemgetter(len(distances[0])-1))

            # find k nearest neighbors
            neighbors = find_neighbors(distances, k)

            # get the class with maximum votes
            index, value = find_response(neighbors, classes)

            # Display prediction
            print('The predicted class for sample ' + str(test_instance) + ' is : ' + classes[index])

            predicted_result = 'The predicted crop is : ' + classes[index]

            distances.clear()

    except Exception as e:
        print(e)

    return classes[index]


def train_crops():
    # try:
        
        training_file = 'data/crop_value_ds_new.csv'
        training_set = convert_to_float(load_data_set(training_file), 'training')
        
        filename = 'crops.pickle'
        outfile = open(filename,'wb')
        pickle.dump(training_set, outfile) 
        outfile.close()



        return training_set


def predict_crop(path):
    
    try:
        k = 5
        
        test_file = path
        data = load_data_set(test_file)

        test_set = convert_to_float(data, 'test')
       
        infile = open("crops.pickle",'rb')
        training_set = pickle.load(infile)
        infile.close()



        if not test_set:
            print('Empty test set provided')
        else:

            result = knn(training_set, test_set, k)

    except ValueError as v:
        print(v)

    except FileNotFoundError:
        print('File not found')

    return result


def newpredict_farmer_cropss(crop_characteristics):
    # print("this is the function")
    try:
        k = 5

        data_set = []
        data_set.clear()
        data_set.append(crop_characteristics) 

        predict_set = convert_to_float(data_set, 'predict')
        print("predictset", predict_set)

        infile = open("crops.pickle",'rb')
        training_set = pickle.load(infile)
        infile.close()
       
        if not predict_set:
            print('Empty test set provided')
        else:
            result = knn(training_set, predict_set, k)

    except ValueError as v:
        print(v)

    except FileNotFoundError:
        print('File not found')

    return result


train_crops()


# predict_farmer_cropss(['49', '14', '8.65', '5.89', '1.4', '0.9', '1.12', '0.4', '1.18', '0.43', '28', '18'])
# newpredict_farmer_cropss(['49', '14', '8.65', '5.89', '1.4', '0.9', '1.12', '0.4', '1.18', '0.43', '28', '18'])