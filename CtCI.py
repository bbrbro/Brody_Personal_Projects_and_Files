# This file contains the solutions and tests for each problem in Cracking the Coding interview
# To use this file, you first need to initialize the class CtCl
# Next initialize the
# To run a particular question, use each is referenced by just the name of the question i.e. CtCl.Is_Unique(inputs)
# Each question will refer to the class CtCl.Unit_Tests.<Name of Function> and print the results of the function and
# each unit test run in that group
# The function CtCl.Run_All(), you guessed it, runs all the Units Tests in the file for each question

def CtCl():

    #Chapter 1 Problems
    def Is_Unique(input,additional_structures):
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
    def Check_Permutation(input):
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
    def URLify(input):
        """
        :param input: is in the format ["string", true length of string: int]
        """
        #takes the first n chars (input[1]) in the string (input[0]) and splits along " " then joins along %20
        return "%20".join(input[0][:input[1]].split(" "))
    def Palindrome_Permutation(input):
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
    def One_Away(input):
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
    def String_Compression(input):
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
    def Rotate_Matrix(input):
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
    def Zero_Matrix(input):
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
    def String_Rotation(input):
        #assuming you have a function which checks if a string is a substring of another, write code to check if s2 is a rotation of s1
        #say s1="waterbottle", s2 = "erbottlewat" - all we need to do is s1+s1, "wat[erbottlewat]erbottle" and make sure the lengths are the same
        if len(input[0])==len(input[1]):
            #it technically asks us to use some method isSubstring but we have 'in'
            return input[1] in input[0] + input[0]
        else:
            return False

    #Chapter 2 Problems
    def Remove_Dups(input):
        if input.next==None:
            return None
        else:
            if input.next==input.next.next:
                input.next = input.next.next
            else:
                input = input.next



    def Kth_to_Last(input):
    def Delete_Middle_Node(input):
    def Partition(input):
    def Sum_Lists(input):
    def Palindrome(input):
    def Intersection(input):
    def Loop_Detection(input):







    def Unit_Tests(self):
        def Is_Unique(self):

        def Check_Permutation(self):

        def URLify(self):

        def Palindrome_Permutation(self):

        def One_Away(self):

        def String_Compression(self):

        def Rotate_Matrix(self):

        def Zero_Matrix(self):

        def String_Rotation(self):

    def Run_All(self):

