# minimax.py
import copy
import math
import utils
import random
import itertools

"""En este archivo se desarrolla el algoritmo minimax."""

def minimax(game, depth, alpha=(-math.inf), beta=(math.inf)):

    
    if depth == 0 or game.blanco.puntaje >= game.objetivo or game.negro.puntaje >= game.objetivo:
        
        # Función de score
        score = game.blanco.puntaje - game.negro.puntaje

        # Caso fin de recursión
        if depth == 0:
            return ((None, None), score)

        # Casos de término
        if game.blanco.puntaje >= game.objetivo and score > 0:
            return ((None, None), math.inf) # Gana blanco
        
        elif game.negro.puntaje >= game.objetivo and score < 0:
            return ((None, None), -math.inf) # Gana negro
        
        elif game.negro.puntaje >= game.objetivo and score == 0:
            return ((None, None), 0) # Empate


    # Se define si se maximiza o minimiza
    maximize = True if game.turno.color == "blanco" else False

    """
    Se deben obtener los posibles movimientos correspondientes a la jugada.
    Los posibles movimientos hay que dejarlos en una lista de tuplas llamada valid_moves.
    valid_moves tendrá elementos del tipo (oveja, fila)
    """
    # Obtener ovejas y filas disponibles
    ovejas_disponibles, filas_disponibles = utils.disponibilidades(game)

    # Generar todos los movimientos válidos (combinaciones de ovejas y filas)
    valid_moves = list(itertools.product(ovejas_disponibles, filas_disponibles))


    if maximize:
        max_score = -math.inf
        best_move = None
        for move in valid_moves:
            game_copy = copy.deepcopy(game)
            # Simula la jugada
            utils.ejecutar_jugada(game_copy, move[0], move[1])

            _, move_score = minimax(game_copy, depth - 1, alpha, beta)

            if move_score > max_score:
                max_score = move_score
                best_move = move

            # actualiza el valor alpha
            alpha = max(alpha, move_score)
            # realiza la poda alpha-beta
            if move_score >= beta:
                break
        
        return (best_move, max_score)
    
    else:
        min_score = math.inf
        best_move = None
        for move in valid_moves:
            game_copy = copy.deepcopy(game)
            # Simula la jugada
            utils.ejecutar_jugada(game_copy, *move)

            _, move_score = minimax(game_copy, depth - 1, alpha, beta)

            if move_score < min_score:
                min_score = move_score
                best_move = move
            
            # actualiza el valor beta
            beta = min(beta, move_score)
            # realiza la poda alpha-beta
            if move_score <= alpha:
                break

        return (best_move, min_score)
    
