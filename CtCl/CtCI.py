# This file contains the solutions and tests for each problem in Cracking the Coding interview
# To use this file, you first need to initialize the class CtCi
# Next initialize the
# To run a particular question, use each is referenced by just the name of the question i.e. CtCi.Is_Unique(inputs)
# Each question will refer to the class CtCi.Unit_Tests.<Name of Function> and print the results of the function and
# each unit test run in that group
# The function CtCi.Run_All(), you guessed it, runs all the Units Tests in the file for each question

class CtCi:

    #Chapter 1 Problems

    def is_unique(self, input, additional_structures = True):
        """
        :param input: in the form "foo"
        :param additional_structures: is a boolean for if we are allowed to use additional data structures
        :return: 
        """
        #Check first if we allow additional data structures
            #True Then we check if the length of the string is equal to the length of the unique hashmap of the string
            #if false we iterate from a point i to the end of a string to check if the same. We can also use any() or _ in _
        if additional_structures:
            if len(input)==len(list(set(input))):
                return True
            else:
                return False
        else:
            for i in range(len(input)):
                for j in range(i+1,len(input)):
                    if input[i]==input[j]:
                        return False
            return True
    def check_permutation(self, input):
        """
        :param input: This should be in the form [string1, string2]
        """
        string1 = input[0]
        string2 = input[1]

        #we can simply count the amount of each character in the string. We will use a dict()
        #subtracting the counts from each other should be all positives or zeros or all negatives

        char_dict = dict()
        for char in string1:
            try:
                char_dict[char] = char_dict[char]+1
            except:
                char_dict[char] = 1

        for char in string2:
            try:
                char_dict[char] = char_dict[char]-1
            except:
                char_dict[char] = -1

        char_values = list(char_dict.values())
        if any(all(char_values>0),all(char_values==0),all(char_values<0)):
            return True
        else:
            return False
    def URLify(self, input):
        """
        :param input: is in the format ["string", true length of string: int]
        """
        #takes the first n chars (input[1]) in the string (input[0]) and splits along " " then joins along %20
        return "%20".join(input[0][:input[1]].split(" "))
    def palindrome_permutation(self, input):
        #check if its a permutation of a palindromw
        #we first must remove all special characters. Then lowercase the string.
        input = ''.join(char.lower() for char in input if char.isalpha())
        #if the count of each character is even expect 1 then its a palindrome otherwise false
        char_dict = dict()
        for char in input:
            try:
                char_dict[char] = char_dict[char]+1
            except:
                char_dict[char] = 1

        if sum(list( char_dict.values() ) % 2) > 1:
            return False
        else:
            return True
    def one_away(self, input):
        """
        :param input: should be in the form [string1, string2]
        """
        #just some precalcs on the length of the strings
        l1 = len(input[0])
        l2 = len(input[1])
        #checks right away that the lengths are not too far apart
        if abs(l2-l1)>1:
            return False
        #checks if any string is empty
        elif l2==0 or l1==0:
            return True
        else:
            pass

        differences = 0
        #if the lengths are the same it means a swap occured, so we can just compare the char's until we hit two differences otherwise it is true
        if l1==l2:
            for i in range(l1):
                if input[0][i]!=input[1][i]:
                    differences+=1
                    if differences == 2:
                        return False
            return True
        #if the length is less it means we did a subtraction so we can compare until we hit a difference and then subtract that from the larger chain until the second difference occurs
        elif l1>l2:
            for i in range(l1):
                if input[0][i]!=input[1][i-differences]:
                    differences+=1
                    if differences == 2:
                        return False
            return True
        # if the length is less it means we did an addition so we can compare until we hit a difference and then subtract that from the larger chain until the second difference occurs
        else:
            for i in range(l2):
                if input[0][i-differences]!=input[1][i]:
                    differences+=1
                    if differences == 2:
                        return False
            return True
    def string_compression(self, input):
        """
        :param input: str "foo"
        :return: original string or compressed string, whichever is shorter
        """
        #if its empty just return it
        if not input:
            return input

        #the first value must be the first char and there must be currently 1 of them
        s = input[0]
        counter=1
        #iterates through the array
        for i in range(1,len(input)):
            #if the value is the same as the last add to the counter otherwise add the counter to the last letter and add the new letter
            if input[i]==input[i-1]:
                counter+=1
            else:
                s+=str(counter)+input[i]
                counter=1
        #check if the new string is shorter and return the smaller
        if len(s)>=len(input):
            return input
        else:
            return s
    def rotate_matrix(self, input):
        """
        :param input: this is in matrix form [[1,2,3],[4,5,6],[7,8,9]]
        """
        n = len(input)  # this is an n by n matrix
        #if we are working with an even matrix e.g. 4x4 this will create a 2x2 loop
        #if we are working with an odd matrix e.g. 5x5 this will create a 2x3 loop. This will leave the middle block alone but take care of the vertical and horizontal middles.
        for i in range(n//2):
            for j in range((n+1)//2):
                #rotates the previous corner into the new position respectively. Keeps track of the first position to be replaced as a tmp values
                tmp                 = input[i    ][j    ]
                input[i    ][j    ] = input[n-1-j][i    ]
                input[n-1-j][i    ] = input[n-1-i][n-1-j]
                input[n-1-i][n-1-j] = input[j    ][n-1-i]
                input[j    ][n-1-i] = tmp
    def zero_matrix(self, input):
        """
        :param input: this is in matrix form [[1,2,3],[4,5,6],[7,8,9]] in range MxN
        """
        m = len(input)
        n = len(input[0])
        #create 1 filled row and column index trackers
        column_zeros = [1]*m
        row_zeros = [1]*n
        for i in range(m):
            for j in range(n):
                #if we detect a zero in the matrix, set its column and row trackers to zero
                if input[i][j]==0:
                    column_zeros[i]=0
                    row_zeros[j]=0
                else:
                    pass

        #for each zero in the column tracker update that row as zeros
        for i in range(m):
            if column_zeros[i]==0:
                input[i]=[0]*n
            else:
                pass
        # for each zero in the row tracker update that column as zeros
        for j in range(n):
            if row_zeros[j]==0:
                for i in range(n):
                    input[i][j]==0
            else:
                pass

        return input
    def string_rotation(self, input):
        #assuming you have a function which checks if a string is a substring of another, write code to check if s2 is a rotation of s1
        #say s1="waterbottle", s2 = "erbottlewat" - all we need to do is s1+s1, "wat[erbottlewat]erbottle" and make sure the lengths are the same
        if len(input[0])==len(input[1]):
            #it technically asks us to use some method isSubstring but we have 'in'
            return input[1] in input[0] + input[0]
        else:
            return False

    #Chapter 2 Problems
    def remove_dups(self, input):
        if input.next==None:
            return None
        else:
            if input.next==input.next.next:
                input.next = input.next.next
            else:
                input = input.next
    def kth_to_last(self, input):
    def delete_middle_node(self, input):
    def partition(self, input):
    def sum_lists(self, input):
    def palindrome(self, input):
    def intersection(self, input):
    def loop_detection(self, input):

    #Chapter 3 Problems
    def three_in_one(self, input):
        #python is particularly good at this. Stacks are obvious.
        stack = input
        r_stack = input[::-1]
        queue = input
        #we can now use stuff like stack[-1] to view the top, we can use stack.pop(), stack.append()
        # we can now use stuff like r_stack[-1] to view the top, we can use r_stack.pop(), r_stack.append()
        # we can now use stuff like queue[_] to view the whatever we need, we can use stack.pop(0), stack.append()
        return stack, r_stack, queue
    def stack_min(self):
        #when we initialize the class we must initialize the stacks
        stack = []
        min_stack = []
        def push(self,input): #if the new number is equal to or smaller than the min, add it both stacks
            stack.append(input)
            if input<=min_stack[-1]:
                min_stack.append(input)
        def pop(self): #if the pop value is the min value remove it from both stacks
            if stack.pop()==min_stack[-1]:
                min_stack.pop()
        def min(self): #just returns the min
            return min_stack[-1]
    def stack_of_plates(self):
        def SetOfStacks(self):
            set_of_stacks = [[]]
            capacity = 5

            def push(self,input):
                if len(self.set_of_stacks[-1])==self.capacity:
                    self.set_of_stacks.append([input])
                else:
                    self.set_of_stacks[-1].append(input)

            def pop(self):#This will always pop, but it might need to remove an empty stack
                self.set_of_stacks[-1].pop()
                if len(self.set_of_stacks[-1])==0:
                    self.set_of_stacks.pop()
    def queue_via_stacks(self):
        def MyQueue(self):
            queue = []
            r_queue = []
            tmp = []
            def add(self,input):
                self.queue.append(input)
                if isEmpty(self.tmp):
                    self.tmp = input
            def remove(self):
                while not isEmpty(self.queue):
                    self.r_queue.append(self.queue.pop())
                self.r_queue.pop()
                self.tmp = self.r_queue[-1]
                while not isEmpty(self.r_queue):
                    queue.append(self.r_queue.pop())

            def peek(self):
                return self.tmp
            def isEmpty(input):
                try:
                    input[-1]
                    return False
                except:
                    return True
    def sort_stack(self, input):
        # we are gonna make a slight modification here, this stack will be input as an array but treated as a stack
        tmp_stack = []
        while len(input)!=0:
            try:
                while input[-1]<tmp_stack[-1]:
                    tmp = input.pop()
                    input.append(tmp_stack.pop())
                    input.append(tmp)
            except:
                pass
            tmp_stack.append(input.pop())
        return tmp_stack
    def animal_shelter(self, input):
        """
        :param input: is in the format "D" or "C"
        """
        #Initiates the queue
        queue = []

        #append to the end
        def enqueue(self,input):
            self.queue.append(input)

        #removes the first element
        def dequeueAny(self):
            self.queue.pop(0)

        #next two functions search for the next D or C in queue and removes that element
        def dequeueDog(self):
            for i in range(len(self.queue)):
                if self.queue[i]=="D":
                    self.queue.pop(i)
                    break

        def dequeueCat(self):
            for i in range(len(self.queue)):
                if self.queue[i]=="C":
                    self.queue.pop(i)
                    break

    #Chapter 4 Problems
    class Node:

        def __init__(self, input):

            self.left = None
            self.right = None
            self.value = input




    def route_between_nodes(self, input, graph): #actually very hard
        """
        :param input: in the form ["S","E"]
        :param graph: in the form of a dictionary
        """
        path_one_queue = [input[0]]
        path_two_queue = [input[1]]
        p1dict = dict()
        p2dict = dict()
        while path_one_queue or path_two_queue:
            while path_one_queue:
                tmp = path_one_queue.pop(0)
                try:
                    p2dict[tmp]
                    return True
                except:
                    try:
                        p1dict[tmp]
                    except:
                        p1dict[tmp] = 1
                        for item in graph[tmp]
                            path_one_queue.append(item)

            while path_two_queue:
                tmp = path_two_queue.pop(0)
                try:
                    p1dict[tmp]
                    return True
                except:
                    try:
                        p2dict[tmp]
                    except:
                        p2dict[tmp] = 1
                        for item in graph[tmp]
                            path_two_queue.append(item)
        return False
    def minimal_tree(self,input):
        #breaks the array into three chunks where the upper of the middle is the node value. Then splits into left and right
        l = len(input)
        node = self.Node(input[l // 2])
        left = input[:l//2]
        right = input[l // 2 + 1:]

        #left will always have at least one so we can either set the value or expand the tree
        if len(left)==1:
            node.left = left
        else:
            node.left = self.minimal_tree(left)

        #right can be empty, one, or more so we need to check
        if len(right)==0:
            pass
        elif len(right)==1:
            node.right = right
        else:
            node.right = self.minimal_tree(right)

        #return the node
        return node
    def list_of_depth(self,input):
        #takes a binary tree and return a linked list for each depth, we assume at least 1 value
        #to start we have an empty list of LL and set the top node as our next queue
        linked_list_list = []
        next_queue = input

        #while there are still next level
        while next_queue:
            #we move the next queue into the current queue
            queue = next_queue[:]
            #and create empty next queue and current linked list
            next_queue = []
            linked_list = []
            while queue:
                #this will remove the array like a queue, add its current value to the linked list
                tmp = queue.pop(0)
                linked_list.append(tmp.value)
                #adds children or roots to the next queue
                if not tmp.left is None:
                    next_queue.append(tmp.left)
                if not tmp.right is None:
                    next_queue.append(tmp.right)
            linked_list_list.append(linked_list)

        return linked_list_list
    def check_balanced(self,input,depth = 0):
        #check if we are at the end, if we are return the depth otherwise check the subtree
        if input.left is None:
            ld = depth
        else:
            ld = check_balanced(input.left, depth = depth + 1)

        #False indicates a trigger so return the trigger
        if ld == False:
            return False

        # check if we are at the end, if we are return the depth otherwise check the subtree
        if input.right is None:
            rd = depth
        else:
            rd = check_balanced(input.right, depth = depth + 1)

        # False indicates a trigger so return the trigger
        if rd == False:
            return False

        #Now we should have depths of the children
        #if the difference between the children sub tree is more than 1 return false
        #Otherwise if we are at node 0, return True, otherwise pass up the max value
        if abs(ld-rd)>1:
            return False
        else:
            if depth ==0:
                return True
            else:
                return max(ld,rd)
    def validate_bst(self, input, depth = 0):

        #if we encounter an empty left or right node, put a (min, max) = (input val, input val)
        #otherwise validate the subtree
        if input.left:
            left_val = validate_bst(input.left, depth = depth + 1)
        else:
            left_val = (input.value,input.value)

        if input.right:
            right_val = validate_bst(input.right, depth = depth + 1)
        else:
            right_val = (input.value,input.value)

        #propogate False upwards
        if left_val==False or right_val==False:
            return False

        #check we want the (min, max) of the left to be less than or equal to the input value
        #and we want input value to be less than the (min, max) of the right tree
        if left_val[0] <= left_val[1] <= input.value <= right_val[0] <= right_val[1]:
            if depth == 0:
                return True
            else:
                return (left_val[0],right_val[1])
        else:
            return False

    def successor():

    def build_order(self, projects, dependencies):

    def first_common_ancestor(self, input):
        #input in shape [node,node]
        #I assume we have a link to the parents
        #I also assume we know the depth
        node1 = input[0]
        node2 = input[1]
        while node1!=node2:
            if node1.depth>=node2.depth:
                node1 = node1.parent
            else:
                node2 = node2.parent
        return node1

    def bst_sequences(self, input):
        #create blank arrays
        new_array, left, right = [], [], []
        #if the node is a deadend, just return the array of itself
        if not input.left and not input.right:
            return [[input.value]]

        #get the permutations of the left branch
        if input.left:
            left = self.bst_sequences(input.left)
        #get the permutations of the right branch
        if input.right:
            right = self.bst_sequences(input.right)

        #checks if there is a blank left or right and shortens calc times
        # the oup
        if not left:
            return [[input.value] + r for r in right]
        elif not right:
            return [[input.value] + l for l in left]
        else:
            for l in left:
                for r in right:
                    new_array.append([input.value]+l+r)
                    new_array.append([input.value]+r+l)
        return new_array

    def check_subtree():
    def random_node():
    def paths_with_sum():





    def Unit_Tests(self):

    def Run_All(self):

