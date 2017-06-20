from django.shortcuts import render, redirect
from django.http import JsonResponse
from operator import itemgetter

from django.contrib.auth.models import User
from squares.models import Square, Board, BoardCell
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required
def BoardView(request):
    try:
        board = Board.objects.get(user=request.user,is_active=True)
    except:
        board = createBoard(request)

    #check if already bingoed
    context = {
        'cells': BoardCell.objects.filter(board=board),
        'bingoed': board.is_bingoed
    }
    return render(request,'squares/board.html', context)

def MarkCell(self, cell_id=None):
    if cell_id:
        cell = BoardCell.objects.get(pk=cell_id)
        cell.marked = not cell.marked
        cell.save()
        marked = cell.marked
        bingoed = checkBingo(cell)
    else:
        marked = false
    return JsonResponse({
        'marked':marked,
        'bingoed':bingoed,
    })

def checkBingo(cell):
    #vars:
    board = cell.board
    x_val = cell.x_val
    y_val = cell.y_val

    #naive checks:
    if not cell.marked:
        return False
    if board.is_bingoed:
        return True

    #check row bingo:
    same_row_count = BoardCell.objects.filter(board=board,x_val=x_val,marked=True).count()
    if same_row_count == 5:
        return markBoardAsBingoed(board)

    #check col bingo:
    same_col_count = BoardCell.objects.filter(board=board,y_val=y_val,marked=True).count()
    if same_col_count == 5:
        return markBoardAsBingoed(board)

    #check left to right diagonal:
    ltr_diag_count = 0;
    for i in range(0,5):
        current_cell = BoardCell.objects.get(board=board,x_val=i,y_val=i)
        if current_cell.marked:
            ltr_diag_count = ltr_diag_count + 1
    if ltr_diag_count == 5:
        return markBoardAsBingoed(board)

    #check right to left diagonal:
    rtl_diag_count = 0;
    for i in range(0,5):
        current_cell = BoardCell.objects.get(board=board,x_val=i,y_val=4-i)
        if current_cell.marked:
            rtl_diag_count = rtl_diag_count + 1
    if rtl_diag_count == 5:
        return markBoardAsBingoed(board)

    return False

def markBoardAsBingoed(board):
    board.is_bingoed = True
    board.save()
    return True

def LogoutView(request):
    logout(request)
    return redirect('login')

def restart(request):
    try:
        current_board = Board.objects.get(user=request.user, is_active=True)
        current_board.is_active = False
        current_board.save()
    finally:
        return redirect('home')

def createBoard(request):
    squares = Square.objects.order_by('?');
    board = Board()
    board.user = request.user
    board.save()
    i = 0
    for s in squares:
        cell = BoardCell()
        cell.board = board
        cell.square = s
        cell.x_val = i % 5
        cell.y_val = i / 5
        if i == 12:
            cell.marked = True
            cell.wildcard = True
        cell.save()
        if i == 24:
            break
        else:
            i = i + 1
    return board

def ScoreBoardView(request):
    users = User.objects.all()
    results = []
    for u in users:
        user_results = {
            'username': u.username,
            'score': BoardCell.objects.filter(board__user=u,marked=True,wildcard=False).count(),
            'bingos': Board.objects.filter(user=u,is_bingoed=True).count(),
        }
        results.append(user_results)
    sorted_results = sorted(results, key=itemgetter('bingos'),reverse=True)
    context = {'results':sorted_results}
    return render(request, 'squares/score_board.html', context)
