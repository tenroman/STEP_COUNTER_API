

class FollowFilter:

    def filter_obj(self):
        filter = {'filter':[{'type':'is_plan', 'id':1, 'status':True}, {'type':'follow_and', 'id':2, 'status':True}]}
        sort = {'sort':[{'type':'is_plan', 'id':3, 'status':True}, {'type':'follow_and', 'id':4, 'status':False}, {'type':'by_name', 'id':5, 'status':False}]}



