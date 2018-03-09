allValidMoves = [];
current_coin = {"row":0,"col":0};
play="X";
opp="O";
final_board_values={};
# whites=[{"row":3,"col":3},{"row":4,"col":5}];
# blacks=[{"row":2,"col":3},{"row":3,"col":4}];

# whites =[{"row":3, "col":3}, {"row":3, "col":5}];
# blacks =[{"row":3, "col":4}];
import os
filename = os.path.dirname(os.path.abspath(__file__)) + '/input5.txt';

with open(filename) as f:
    lines = f.readlines()

first_player = lines[0][:1];
if(first_player == "W"):
    second_player = "B";
else:
    second_player = "W";
DEPTH = int(lines[1][:1]);
initial_board = [];
for i in range(2,10):
	initial_board.append(lines[i][:8]);
# print(initial_board);

def update_WhiteBlack(board):
	new_whites=[];
	new_blacks=[];
	for i in range(0,8):
		for j in range(0,8):
			if(board[i][j]=="X"):
				new_blacks.append({"row":i,"col":j});
			elif(board[i][j]=="O"):
				new_whites.append({"row":i,"col":j});
	return ({"whites":new_whites,"blacks":new_blacks});

bw = update_WhiteBlack(initial_board);
whites = bw["whites"];
blacks = bw["blacks"];

def traverseRecursively(current_board,coin,row_col):
	global allValidMoves;
	global current_coin;
	global play;
	global opp;
	row=row_col["row"];
	col=row_col["col"];
	new_row=coin["row"]+row;
	new_col=coin["col"]+col;

	if(new_row>7 or new_col>7 or new_row<0 or new_col<0 or (current_board[new_row][new_col]==play)):
		return False;
	if(current_board[new_row][new_col]=="*" and ((current_coin["row"]+row)==new_row) and ((current_coin["col"]+col)==new_col)):
		return False;
	if(current_board[new_row][new_col]==opp):
		coin={"row":new_row,"col":new_col};
		coin_temp=coin;
		current_board[new_row][new_col]=play;
		current_board_temp1=current_board;
		traverseRecursively(current_board_temp1[:],coin_temp,{"row":row,"col":col});
	else:
		if((new_row + row < 8) and (new_col + col < 8) and (new_row + row >= 0) and (new_col + col >= 0)):
			current_board[new_row][new_col] = play;
			adjacent_coin = {"row": new_row, "col": new_col};
			current_board_temp=current_board;
			row_col_temp=row_col;
			adjacent_coin_temp=adjacent_coin;
			allValidMoves.append({"board":current_board_temp, "move": row_col_temp, "coin": adjacent_coin_temp});
		else:
			return False;

def getAllValidMoves(board,players,opponents,color):
	global allValidMoves;
	global final_board_values;
	global play;
	global opp;
	global allValidMoves;
	global current_coin;
	allValidMoves=[];
	play='X';
	opp='O';
	if(color=="W"):
		play='O';
		opp='X';
	possible_movements = [
    {"row":-1, "col":-1}, {"row":-1, "col":0}, {"row":-1, "col":1},
    {"row":0, "col":-1}, {"row":0, "col":1},
    {"row":1, "col":-1}, {"row":1, "col":0}, {"row":1, "col":1},
  	];
	board_temp=board;
	length = len(players);
	for j in range(0,length):
		board_temp = board;
		current_coin=players[j];
		for i in range(0,len(possible_movements)):
			traverseRecursively(create_board(),current_coin,possible_movements[i]);
	return allValidMoves;

def create_board():
	board=[];
	for i in range(0,8):
		board.append(['*','*','*','*','*','*','*','*']);
		for j in range(0,8):
			ele={"row":i, "col":j};
			if(ele in blacks):
				board[i][j] = 'X';
			elif(ele in whites):
				board[i][j] = 'O';
			else:
				board[i][j] = '*';
	return board;

def checkForPassMove(board):
	x = False;
	y = False;
	z = False;
	for i in range(0,8):
		for j in range(0,8):
			if(board[i][j] == 'X'):
				x = True;
			elif(board[i][j] == 'O'):
				y = True;
			else:
				z = True;
			if(x and y and z):
				return [{"board": board}];
	return [];

def getMove(coin):
	col = coin["col"];
	row = coin["row"];
	if(col == 0):
		return "a"+str(row+1);
	if(col == 1):
		return "b"+str(row+1);
	if(col == 2):
		return "c"+str(row+1);
	if(col == 3):
		return "d"+str(row+1);
	if(col == 4):
		return "e"+str(row+1);
	if(col == 5):
		return "f"+str(row+1);
	if(col == 6):
		return "g"+str(row+1);
	if(col == 7):
		return "h"+str(row+1);

root={
	"key":"root", "parent":None, "children":[],
	"value":None, "alpha":None, "beta":None,
	"state":create_board(), "level":0, "move":"root"
};

child_Nodes=[root];
all_childs_at_depth={"root":root};
all_keys=["root"];
pass_flag = 0;
for i in range(1,DEPTH+1):
	temp_nodes_array=[];
	for j in range(0,len(child_Nodes)):
		some_move = "";
		coins=update_WhiteBlack(child_Nodes[j]["state"]);
		whites=coins["whites"];
		blacks=coins["blacks"];
        if(i%2==1):
            player_tmp = first_player;
        else:
            player_tmp = second_player;
        if(player_tmp == "W"):
            pl = whites;
            op = blacks;
        else:
            pl = blacks;
            op = whites;
        children_now = getAllValidMoves(create_board(),pl,op,player_tmp);
		#check for pass move
    	if(len(children_now) == 0):
            if(pass_flag < 2):
                pass_flag = pass_flag+1;
                children_now = [{"board":create_board()}];
                some_key = child_Nodes[j]["key"] + "->pas";
                some_move = "pass";
    	for child in children_now:
            if(not "pass" == some_move):
                some_key = child_Nodes[j]["key"] + "->" + str(child["coin"]["row"]) + "," + str(child["coin"]["col"]);
                some_move = getMove(child["coin"]);
                pass_flag = 0;
            temp_nodes_array.append({
                "key":some_key, "parent":child_Nodes[j]["key"], "children":[],
                "value":None, "alpha":None, "beta":None,
                "level":i, "state":child["board"], "move":some_move});
            all_childs_at_depth[child_Nodes[j]["key"]]["children"].append(some_key);
            all_keys.append(some_key);
            all_childs_at_depth[some_key] = temp_nodes_array[len(temp_nodes_array)-1];

        child_Nodes = temp_nodes_array[:];

all_keys.sort();
# print(all_keys);

allMovesInTraversal = ['root'];
for i in range(1,len(all_keys)):
	if(all_keys[i-1] in all_keys[i]):
		allMovesInTraversal.append(all_keys[i]);
	else:
		some_key_now = all_keys[i-1];
		while(not some_key_now in all_keys[i]):
			some_key_now = some_key_now[:-5];
		  	allMovesInTraversal.append(some_key_now);

		allMovesInTraversal.append(all_keys[i]);

# print('final_traversal',allMovesInTraversal);

WEIGHTS = [
[99, -8, 8, 6, 6, 8, -8, 99],
[-8, -24, -4, -3, -3, -4, -24, -8],
[8, -4, 7, 4, 4, 7, -4, 8],
[6, -3, 4, 0, 0, 4, -3, 6],
[6, -3, 4, 0, 0, 4, -3, 6],
[8, -4, 7, 4, 4, 7, -4, 8],
[-8, -24, -4, -3, -3, -4, -24, -8],
[99, -8, 8, 6, 6, 8, -8, 99]
];

_ALPHA = -99999;
_BETA = 99999;
all_childs_at_depth["root"]["alpha"] = _ALPHA;
all_childs_at_depth["root"]["beta"] = _BETA;

def findWeightOfBoard(board):
	checkFor = 'X';
	value = 0;
	if(first_player == 'W'):
		checkFor = 'O';
	for i in range(0,8):
		for j in range(0,8):
			if(board[i][j] == '*'):
				continue
			if(board[i][j] == checkFor):
				value = value + WEIGHTS[i][j];
			else:
				value = value - WEIGHTS[i][j];
	return value;

def maximiser(key):
	if(all_childs_at_depth[key]["alpha"] <= all_childs_at_depth[key]["value"]):
		all_childs_at_depth[key]["alpha"] = all_childs_at_depth[key]["value"];

def minimiser(key):
	if(all_childs_at_depth[key]["beta"] >= all_childs_at_depth[key]["value"]):
		all_childs_at_depth[key]["beta"] = all_childs_at_depth[key]["value"];

def updateAlphaBetaForLeaf(key):
	all_childs_at_depth[key]["value"] = findWeightOfBoard(all_childs_at_depth[key]["state"]);
	# if(all_childs_at_depth[key]["level"] % 2 == 0):
	# 	maximiser(key);
	# else:
	# 	minimiser(key);

def parent_node_value(key, code):
	children = all_childs_at_depth[key]["children"];
	max = None;
	min = None;
	for i in range(0, len(children)):
		if(all_childs_at_depth[children[i]]["value"] == None):
			all_children_traversed = False;
			continue;
		if(max == None):
			max = all_childs_at_depth[children[i]]["value"];
			min = all_childs_at_depth[children[i]]["value"];
		else:
			if(all_childs_at_depth[children[i]]["value"] > max):
				 max = all_childs_at_depth[children[i]]["value"];
 			if(all_childs_at_depth[children[i]]["value"] < min):
 				 min = all_childs_at_depth[children[i]]["value"];
	if(code == 'MAX'):
		return max;
	return min;

def updateAlphaBetaForParent(key):
	if(all_childs_at_depth[key]["level"] % 2 == 0):
		all_childs_at_depth[key]["value"] = parent_node_value(key, 'MAX');
		maximiser(key);
	else:
		all_childs_at_depth[key]["value"] = parent_node_value(key, 'MIN');
		minimiser(key);
sequence = ''
f = open('output.txt', 'w');
# print('Node,Depth,Value,Alpha,Beta');
sequence+=('Node,Depth,Value,Alpha,Beta\n');
# print('root,0,-Infinity,-Infinity,Infinity');
sequence+=('root,0,-Infinity,-Infinity,Infinity\n');

skip = 0;
for i in range(1, len(allMovesInTraversal)):
	if(i<=skip):
		continue;
	if(all_childs_at_depth[allMovesInTraversal[i]]["parent"] == allMovesInTraversal[i-1]):
		# print('parent to child',allMovesInTraversal[i]);
		all_childs_at_depth[allMovesInTraversal[i]]["alpha"] = all_childs_at_depth[allMovesInTraversal[i-1]]["alpha"];
		all_childs_at_depth[allMovesInTraversal[i]]["beta"] = all_childs_at_depth[allMovesInTraversal[i-1]]	["beta"];
		if(len(all_childs_at_depth[allMovesInTraversal[i]]["children"]) == 0):
			updateAlphaBetaForLeaf(allMovesInTraversal[i]);
		else:
			if(all_childs_at_depth[allMovesInTraversal[i]]["level"] %2 == 0):
				all_childs_at_depth[allMovesInTraversal[i]]["value"] = all_childs_at_depth[allMovesInTraversal[i]]["alpha"];
			else:
				all_childs_at_depth[allMovesInTraversal[i]]["value"] = all_childs_at_depth[allMovesInTraversal[i]]["beta"];
	else:
		# print('child to parent',allMovesInTraversal[i]);
		updateAlphaBetaForParent(allMovesInTraversal[i]);
		if(all_childs_at_depth[allMovesInTraversal[i]]["alpha"] >= all_childs_at_depth[allMovesInTraversal[i]]["beta"]):
			branch_to_be_pruned = allMovesInTraversal[i];
			# print(branch_to_be_pruned + ' GOT PRUNED !!!!');
			if(i == (len(allMovesInTraversal)-2)):
				break;
			while(branch_to_be_pruned in allMovesInTraversal[i+1]):
				i=i+1;
				skip = i;
	# print('@node: ',allMovesInTraversal[i]);
	# values_here = getNodeValues();	#get alpha, beta and node values
	sequence+=((all_childs_at_depth[allMovesInTraversal[i]]["move"] + ',' +
		str(all_childs_at_depth[allMovesInTraversal[i]]["level"]) + ',' +
		str(all_childs_at_depth[allMovesInTraversal[i]]["value"]).replace('99999','Infinity')+ ',' +
		str(all_childs_at_depth[allMovesInTraversal[i]]["alpha"]).replace('99999','Infinity')+ ',' +
		str(all_childs_at_depth[allMovesInTraversal[i]]["beta"]).replace('99999','Infinity')+ '\n')
	);
final_traversal = allMovesInTraversal[len(allMovesInTraversal)-1];
while(not ('root' == final_traversal)):
	final_traversal = final_traversal[:-5];
	updateAlphaBetaForParent(final_traversal);
	sequence+=(all_childs_at_depth[final_traversal]["move"] + ',' +
		str(all_childs_at_depth[final_traversal]["level"]) + ',' +
		str(all_childs_at_depth[final_traversal]["value"]).replace('99999','Infinity')+',' +
		str(all_childs_at_depth[final_traversal]["alpha"]).replace('99999','Infinity')+',' +
		str(all_childs_at_depth[final_traversal]["beta"]).replace('99999','Infinity')+ '\n'
	);
for child in all_childs_at_depth["root"]["children"]:
    if(all_childs_at_depth[child]["value"] == all_childs_at_depth["root"]["value"]):
        for i in range(0,8):
            for j in range(0,8):
                f.write(all_childs_at_depth[child]["state"][i][j]);
            f.write("\n");

f.write(sequence);
f.close();
