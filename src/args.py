import argparse

def program_args(): 
    ''' 
    param: 
    -c, --controller controller options, user or AI   
    -r, --render render bird options 
    return: args 
    '''
    parser = argparse.ArgumentParser(
        description= ''
    )
    # Sample argument: 
    # parser.add_argument('-r',
    #                     '--rectangle', 
    #                     help = 'draw rectangle delimiting target surface on frame', 
    #                     action = 'store_true')
    args = parser.parse_args()
    return args 

