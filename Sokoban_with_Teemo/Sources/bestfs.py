import support_function as spf 
import time
import os
from queue import PriorityQueue

'''
//========================//
//    BEST FIRST SEARCH   //
//        ALGORITHM       //
//     IMPLEMENTATION     //
//========================//
'''
def BestFS_Search(board, list_check_point):
    start_time = time.time()
    ''' BESTFS SEARCH SOLUTION '''
    ''' IF START BOARD IS GOAL OR DON'T HAVE CHECK POINT '''
    if spf.check_win(board,list_check_point):
        print("Found win")
        return [board]
    ''' INITIALIZE START STATE '''
    start_state = spf.state(board, None, list_check_point)
    list_state = [start_state]
    ''' INITIALIZE PRIORITY QUEUE '''
    heuristic_queue = PriorityQueue()
    heuristic_queue.put(start_state)
    ''' LOOP THROUGH PRIORITY QUEUE '''
    while not heuristic_queue.empty():
        '''GET NOW STATE TO SEARCH'''
        now_state = heuristic_queue.get()
        ''' GET THE PLAYER'S CURRENT POSITION'''
        cur_pos = spf.find_position_player(now_state.board)
        ''' 
        THIS WILL PRINT THE STEP-BY-STEP IMPLEMENTATION OF HOW THE ALGORITHM WORKS, 
        UNCOMMENT TO USE IF NECCESSARY 
        '''
        
        time.sleep(0)
        clear = lambda: os.system('cls')
        clear()
        #print_matrix(now_state.board)
        print("State visited : {}".format(len(list_state)))
        
        ''' GET LIST POSITION THAT PLAYER CAN MOVE TO '''
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        ''' MAKE NEW STATES FROM LIST CAN MOVE '''
        for next_pos in list_can_move:
            ''' MAKE NEW BOARD '''
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
            ''' IF THIS BOARD DON'T HAVE IN LIST BEFORE --> SKIP THE STATE '''
            if spf.is_board_exist(new_board, list_state):
                continue
            ''' IF ONE OR MORE BOXES ARE STUCK IN THE CORNER --> SKIP THE STATE '''
            if spf.is_board_can_not_win(new_board, list_check_point):
                continue
            ''' IF ALL BOXES ARE STUCK --> SKIP THE STATE '''
            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            ''' MAKE NEW STATE '''
            new_state = spf.state(new_board, now_state, list_check_point)
            ''' CHECK WHETHER THE NEW STATE IS GOAL OR NOT '''
            if spf.check_win(new_board, list_check_point):
                print("Found win")
                print("The number of state visited:",len(list_state))
                print("The number of step:",len(new_state.get_line())-1)
                return (new_state.get_line(), len(list_state))
            
            ''' APPEND NEW STATE TO PRIORITY QUEUE AND TRAVERSED LIST '''
            list_state.append(new_state)
            heuristic_queue.put(new_state)
            print("The number of step:{}".format(len(new_state.get_line())-1)) #Static
            
            ''' COMPUTE THE TIMEOUT '''
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []
    ''' SOLUTION NOT FOUND '''
    print("Not Found")
    return []