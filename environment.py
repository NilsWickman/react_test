import torch

class env():
    def __init__(self):
        self.reward = 0
        self.done = False
        self.game_state = torch.full((6, 7), 0.5)
        self.active_player = False
        self.legal = False

    def step(self, action):
        self.active_player = True
        if self.check_legality(action) == False:
            self.reward = -1000
            self.done = True
            return self.game_state, self.reward, self.done

        self.game_state[action - 1] = 0.0
        self.legal = False

        if self.check_draw():
            return self.game_state, self.reward, self.done
        if self.check_win():
            return self.game_state, self.reward, self.done

        #Random Game Action
        while self.legal:
            random_action = torch.randint(1, 8, (1,)).item()
            self.check_legality(random_action)
        self.active_player = False
        self.game_state[random_action - 1] = 1.0
        if self.check_draw():
            return self.game_state, self.reward, self.done
        if self.check_win():
            return self.game_state, self.reward, self.done
        

        return self.game_state, self.reward, self.done

    def reset(self):
        self.done = False
        self.game_state = torch.full((6, 7), 0.5)
        return self.game_state

    def check_win(self):
        tensor = self.game_state

        if self.four_in_a_row():
            self.done = True
            if self.active_player:
                self.reward = 100
            else:
                self.reward = -100
            return True

        return False

    def check_draw(self):
        if (self.game_state[0, :] == 0.5).any().item():
            self.done = True
            return True
        else:
            return False

    def four_in_a_row(self):
        tensor = self.game_state
        for row in range(tensor.size(0)):
            for column in range(tensor.size(1)):
                if row + 4 < tensor.size(0):
                    if tensor[row][column] + tensor[row + 1][column] + tensor[row + 2][column] + tensor[row + 3][column] == 4.0 or 0.0:
                        return True
                if column + 4 < tensor.size(1):
                    if tensor[row][column] + tensor[row][column + 1] + tensor[row][column + 2] + tensor[row][column + 3] == 4.0 or 0.0:
                        return True
                if column + 4 < tensor.size(1) and row + 4 < tensor.size(0):
                    if tensor[row][column] + tensor[row + 1][column + 1] + tensor[row + 2][column + 2] + tensor[row + 3][column + 3] == 4.0 or 0.0:
                        return True
                if column + 4 < tensor.size(1) and row - 4 > 0:
                    if tensor[row][column] + tensor[row - 1][column + 1] + tensor[row - 2][column + 2] + tensor[row - 3][column + 3] == 4.0 or 0.0:
                        return True
        return False

    def check_legality(self, action):
        if self.game_state[action - 1][-1] != 0.5:
            self.legal = False
            return self.legal
        else:
            self.legal = True
            return self.legal
