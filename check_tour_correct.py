def charnum(astring):
    m = len(astring)
    dumlist = []
    if m != 0:
        for i in range(0, m):
            if ord(astring[i]) >= 48 and ord(astring[i]) <= 57:
                dumlist.append(astring[i])
        astring = ""
        if len(dumlist) != 0:
            for i in range(0, len(dumlist)):
                astring = astring + dumlist[i]
    if astring == "":
        astring = "0"
    return astring


def tc(inputfile, inputtourfile):
    f = open(inputfile, 'r')  # read in data character by character
    x = f.read(1)  # and strip away rubbish
    flag = "good"
    d = ""
    while x != "":
        if ord(x) >= 44 and ord(x) <= 122:
            d = d + x
        x = f.read(1)
    f.close()

    start_of_name = d.find("NAME")  # check that NAME=<city file-name>, appears
    if start_of_name == -1:
        flag = "error: no city-file name"
        print(flag + "\n")
    else:
        comma_after_name = d.find(",", start_of_name)
        if comma_after_name == -1:
            flag = "error: no comma after NAME="
            print(flag + "\n")
        else:
            name = d[start_of_name + 5:comma_after_name]  # get city name

    if flag[0] != "e":
        start_of_size = d.find("SIZE=", comma_after_name)  # check that SIZE=<number of cities>, appears
        if start_of_size == -1:
            flag = "error: no SIZE="
            print(flag + "\n")
        else:
            comma_after_size = d.find(",", start_of_size)
            if comma_after_size == -1:
                flag = "error: no comma after SIZE="
                print(flag + "\n")
            else:
                w = charnum(d[start_of_size + 5:comma_after_size])  # get number of sities
                n = int(w)

    if flag[0] != "e":
        start = comma_after_size + 1  # compute distances
        end = len(d)
        first_character = start
        row = [0]
        matrix = []
        current_row = 1
        current_column = 2
        if first_character >= end:
            jumpout = "yes"
        else:
            jumpout = "no"
        while jumpout == "no" and current_row <= n - 1:  # iteratively get numbers between commas
            next_comma = d.find(",", first_character)
            if next_comma != -1:
                step = int(charnum(d[first_character:next_comma]))
                first_character = next_comma + 1
            else:
                if first_character < end:
                    step = int(charnum(d[first_character:end]))
                    jumpout == "nearly"
                else:
                    jumpout = "yes"
            if jumpout != "yes":
                row.append(step)  # add distance to matrix
                current_column = current_column + 1
                if current_column == n + 1:  # add in dummy 0s
                    matrix.append(row)
                    row = [0]
                    current_row = current_row + 1
                    for k in range(1, current_row):
                        row.append(0)
                    current_column = current_row + 1
        if current_row <= n - 1:
            jumpout == "yes"
        if jumpout == "yes":
            flag = "error: too few distances supplied (up to [" + str(row) + "," + str(column) + "]"
            print(flag + "\n")
        else:
            row = [0]
            for j in range(1, n):  # add on row of 0's
                row.append(0)
            matrix.append(row)
            for i in range(2, n + 1):  # make matrix symmetric
                for j in range(1, i):
                    matrix[i - 1][j - 1] = matrix[j - 1][i - 1]

    if flag[0] != "e":
        f = open(inputtourfile, 'r')
        checklength = 0
        length = 0
        x = f.read(1)
        flag = "good"
        d = ""
        while x != "":
            if ord(x) >= 44 and ord(x) <= 122:
                d = d + x
            x = f.read(1)
        f.close()

        start_of_name = d.find("NAME")  # look for city name
        if d.find("NAME=") == -1:
            flag = "error: no NAME= in tour-file"
            print(flag + "\n")
        else:
            comma_after_name = d.find(",", d.find("NAME="))
            if comma_after_name == -1:
                flag = "error: no comma after NAME= in tour-file"
                print(flag + "\n")
            else:
                tname = d[start_of_name + 5:comma_after_name]
                if name != tname:
                    flag = "error: name of city-file and tour-file don't match (city: " + name + " and tour: " + tname + ")"
                    print(flag + "\n")

        if flag[0] != "e":  # look for number of cities
            start_of_size = d.find("SIZE=", comma_after_name)
            if start_of_size == -1:
                flag = "error: no SIZE= in tour-file"
                print(flag + "\n")
            else:
                comma_after_size = d.find(",", d.find("SIZE="))
                if comma_after_size == -1:
                    flag = "error: no comma after SIZE= in tour-file"
                    print(flag + "\n")
                else:
                    tn = int(charnum(d[start_of_size + 5:comma_after_size]))
                    if tn != n:
                        flag = "error: numbers of cities mismatch (city size: " + str(n) + ", tour size: " + str(
                            tn) + ")"
                        print(flag + "\n")

        if flag[0] != "e":  # look for tour length
            start_of_length = d.find("LENGTH=")
            if start_of_length == -1:
                flag = "error: no LENGTH= in tour-file"
                print(flag + "\n")
            else:
                comma_after_length = d.find(",", d.find("LENGTH="))
                if comma_after_length == -1:
                    flag = "error: no comma after LENGTH= in tour-file"
                    print(flag + "\n")
                else:
                    length = int(charnum(d[start_of_length + 7:comma_after_length]))

        if flag[0] != "e":  # check tour length
            start_digit = d.find(",", d.find("LENGTH=")) + 1
            end = len(d)
            city_count = 0
            tour = []
            if start_digit >= end:
                jumpout = "yes"
            else:
                jumpout = "no"
            while jumpout == "no" and city_count < n:  # iteratively get the next tour city
                next_comma = d.find(",", start_digit)
                if next_comma != -1:
                    step = int(charnum(d[start_digit:next_comma]))
                    if (step < 1) or (step > n):
                        jumpout = "yes"
                    else:
                        start_digit = next_comma + 1
                else:
                    if start_digit < end:
                        step = int(charnum(d[start_digit:end]))
                        if (step < 1) or (step > n):
                            jumpout = "yes"
                        else:
                            jumpout = "nearly"
                    else:
                        jumpout = "yes"
                if jumpout != "yes":
                    tour.append(step)
                    city_count = city_count + 1
            if city_count != n:
                flag = "error: not enough cities in tour (only " + str(city_count) + ", should be " + str(n) + ")"
                print(flag + "\n")
            else:
                column_city = 0  # compute actual tour length
                jumpout = "no"
                while jumpout == "no" and column_city < n - 1:
                    row_city = column_city + 1
                    while jumpout == "no" and row_city < n:
                        if tour[column_city] == tour[row_city]:
                            jumpout = "yes"
                        else:
                            row_city = row_city + 1
                    column_city = column_city + 1
                if jumpout == "yes":
                    flag = "error: repetition in tour (city " + str(tour[row_city]) + ")"
                    print(flag + "\n")
                else:
                    checklength = 0
                    for j in range(0, n - 1):
                        checklength = checklength + matrix[tour[j] - 1][tour[j + 1] - 1]
                    checklength = checklength + matrix[tour[n - 1] - 1][tour[0] - 1]
                    if checklength != length:
                        flag = "error: tour lengths don't match (claimed length: " + str(
                            length) + ", actual length: " + str(checklength) + ")"
                        print(flag + "\n")
                    else:
                        flag = "good (length of tour is " + str(length) + ")"
                        print(flag + "\n")
                        return [length]

    return [0]


tc('NEWAISearchfile042.txt', 'tourAISearchfile042.txt')