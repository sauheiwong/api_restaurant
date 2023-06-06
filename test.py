my_dic = {
        0:{
            'id': 1,
            'number': 2
        },
        1: {
            'id': 2,
            'number': 4
        },
        2: {
            'id': 5,
            'number': 1
        },
        3: {
            'id': 6,
            'number': 3
        },
}
print(my_dic, max(my_dic), my_dic.values())
my_dic.pop(2)
print(my_dic, max(my_dic), my_dic.values())
