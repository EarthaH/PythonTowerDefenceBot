# -*- coding: utf-8 -*-
'''
Entelect StarterBot for Python3
'''
import time

startTime = time.time()

import json
import os
from time import sleep
import random
    
class StarterBot:
    
    def __init__(self,state_location):
        '''
        Initialize Bot.
        Load all game state information.
        '''
        try:
            self.game_state = self.loadState(state_location)
        except IOError:
            print("Cannot load Game State")
            
        self.full_map = self.game_state['gameMap']
        self.rows = self.game_state['gameDetails']['mapHeight']
        self.columns = self.game_state['gameDetails']['mapWidth']
        self.command = ''
        
        self.player_buildings = self.getPlayerBuildings()
        self.opponent_buildings = self.getOpponentBuildings()
        self.projectiles = self.getProjectiles()
        
        self.player_info = self.getPlayerInfo('A')
        self.opponent_info = self.getPlayerInfo('B')
        
        self.round = self.game_state['gameDetails']['round']
        self.energy = self.player_info['energy']
        
        self.buildings_stats = {"ATTACK":{"health": self.game_state['gameDetails']['buildingsStats']['ATTACK']['health'],
                                 "constructionTime": self.game_state['gameDetails']['buildingsStats']['ATTACK']['constructionTime'],
                                 "price": self.game_state['gameDetails']['buildingsStats']['ATTACK']['price'],
                                 "weaponDamage": self.game_state['gameDetails']['buildingsStats']['ATTACK']['weaponDamage'],
                                 "weaponSpeed": self.game_state['gameDetails']['buildingsStats']['ATTACK']['weaponSpeed'],
                                 "weaponCooldownPeriod": self.game_state['gameDetails']['buildingsStats']['ATTACK']['weaponCooldownPeriod'],
                                 "energyGeneratedPerTurn": self.game_state['gameDetails']['buildingsStats']['ATTACK']['energyGeneratedPerTurn'],
                                 "destroyMultiplier": self.game_state['gameDetails']['buildingsStats']['ATTACK']['destroyMultiplier'],
                                 "constructionScore": self.game_state['gameDetails']['buildingsStats']['ATTACK']['constructionScore']},
                       "DEFENSE":{"health": self.game_state['gameDetails']['buildingsStats']['DEFENSE']['health'],
                                 "constructionTime": self.game_state['gameDetails']['buildingsStats']['DEFENSE']['constructionTime'],
                                 "price": self.game_state['gameDetails']['buildingsStats']['DEFENSE']['price'],
                                 "weaponDamage": self.game_state['gameDetails']['buildingsStats']['DEFENSE']['weaponDamage'],
                                 "weaponSpeed": self.game_state['gameDetails']['buildingsStats']['DEFENSE']['weaponSpeed'],
                                 "weaponCooldownPeriod": self.game_state['gameDetails']['buildingsStats']['DEFENSE']['weaponCooldownPeriod'],
                                 "energyGeneratedPerTurn": self.game_state['gameDetails']['buildingsStats']['DEFENSE']['energyGeneratedPerTurn'],
                                 "destroyMultiplier": self.game_state['gameDetails']['buildingsStats']['DEFENSE']['destroyMultiplier'],
                                 "constructionScore": self.game_state['gameDetails']['buildingsStats']['DEFENSE']['constructionScore']},
                       "ENERGY":{"health": self.game_state['gameDetails']['buildingsStats']['ENERGY']['health'],
                                 "constructionTime": self.game_state['gameDetails']['buildingsStats']['ENERGY']['constructionTime'],
                                 "price": self.game_state['gameDetails']['buildingsStats']['ENERGY']['price'],
                                 "weaponDamage": self.game_state['gameDetails']['buildingsStats']['ENERGY']['weaponDamage'],
                                 "weaponSpeed": self.game_state['gameDetails']['buildingsStats']['ENERGY']['weaponSpeed'],
                                 "weaponCooldownPeriod": self.game_state['gameDetails']['buildingsStats']['ENERGY']['weaponCooldownPeriod'],
                                 "energyGeneratedPerTurn": self.game_state['gameDetails']['buildingsStats']['ENERGY']['energyGeneratedPerTurn'],
                                 "destroyMultiplier": self.game_state['gameDetails']['buildingsStats']['ENERGY']['destroyMultiplier'],
                                 "constructionScore": self.game_state['gameDetails']['buildingsStats']['ENERGY']['constructionScore']}}
        return None
        
        
    def loadState(self,state_location):
        '''
        Gets the current Game State json file.
        '''
        return json.load(open(state_location,'r'))

    def getPlayerInfo(self,playerType):
        '''
        Gets the player information of specified player type
        '''
        for i in range(len(self.game_state['players'])):
            if self.game_state['players'][i]['playerType'] == playerType:
                return self.game_state['players'][i]
            else:
                continue        
        return None
    
    def getOpponentBuildings(self):
        '''
        Looks for all buildings, regardless if completed or not.
        0 - Nothing
        1 - Attack Unit
        2 - Defense Unit
        3 - Energy Unit
        '''
        opponent_buildings = []
        
        for row in range(0,self.rows):
            buildings = []
            for col in range(int(self.columns/2),self.columns):
                if (len(self.full_map[row][col]['buildings']) == 0):
                    buildings.append(0)
                elif (self.full_map[row][col]['buildings'][0]['buildingType'] == 'ATTACK'):
                    buildings.append(1)
                elif (self.full_map[row][col]['buildings'][0]['buildingType'] == 'DEFENSE'):
                    buildings.append(2)
                elif (self.full_map[row][col]['buildings'][0]['buildingType'] == 'ENERGY'):
                    buildings.append(3)
                else:
                    buildings.append(0)
                
            opponent_buildings.append(buildings)
            
        return opponent_buildings
    
    def getPlayerBuildings(self):
        '''
        Looks for all buildings, regardless if completed or not.
        0 - Nothing
        1 - Attack Unit
        2 - Defense Unit
        3 - Energy Unit
        '''
        player_buildings = []
        
        for row in range(0,self.rows):
            buildings = []
            for col in range(0,int(self.columns/2)):
                if (len(self.full_map[row][col]['buildings']) == 0):
                    buildings.append(0)
                elif (self.full_map[row][col]['buildings'][0]['buildingType'] == 'ATTACK'):
                    buildings.append(1)
                elif (self.full_map[row][col]['buildings'][0]['buildingType'] == 'DEFENSE'):
                    buildings.append(2)
                elif (self.full_map[row][col]['buildings'][0]['buildingType'] == 'ENERGY'):
                    buildings.append(3)
                elif (self.full_map[row][col]['buildings'][0]['buildingType'] == 'TESLA'):
                    buildings.append(4)
                else:
                    buildings.append(0)
                
            player_buildings.append(buildings)
            
        return player_buildings
    
    def getProjectiles(self):
        '''
        Find all projectiles on the map.
        0 - Nothing there
        1 - Projectile belongs to player
        2 - Projectile belongs to opponent
        '''
        projectiles = []
        
        for row in range(0,self.rows):
            temp = []
            for col in range(0,self.columns):
                if (len(self.full_map[row][col]['missiles']) == 0):
                    temp.append(0)
                elif (self.full_map[row][col]['missiles'][0]['playerType'] == 'B'):
                    temp.append(2)
                else:
                    temp.append(1)
                
            projectiles.append(temp)
            
        return projectiles

    def checkProjectiles(self, lane_number):
        lane = list(self.projectiles[lane_number])
        if (lane.count(2) > 0):
            return True
        else:
            return False
    
    def shouldDefend(self):
        ret_col = -1

        if self.energy < 30:
            return -1,-1

        for col in range(4,8):
            if self.checkProjectiles(col) and not self.checkFirstDefense(col) and not self.checkMyAttack(col):
                return col,0
        for col in range(8):
            if self.checkAttack(col) and not self.checkFirstDefense(col):
                return col,1
            if self.checkAttack(col) and not self.checkSecondDefense(col):
                ret_col = col
        
        if ret_col > -1:
            return ret_col,2

        return ret_col,-1


    def checkDefense(self, lane_number):

        '''
        Checks a lane.
        Returns True if lane contains defense unit.
        '''
        
        lane = list(self.opponent_buildings[lane_number])
        if (lane.count(2) > 0):
            return True
        else:
            return False

    def checkMyDefense(self, lane_number):

        '''
        Checks a lane.
        Returns True if lane contains defense unit.
        '''
        
        lane = list(self.player_buildings[lane_number])
        if (lane.count(2) > 0):
            return True
        else:
            return False

    def checkFirstDefense(self, lane_number):
    
        '''
        Checks a lane.
        Returns True if lane contains defense unit.
        '''
        
        lane = list(self.player_buildings[lane_number])
        if (lane[7] > 0):
            return True
        else:
            return False

    
    def checkSecondDefense(self, lane_number):
    
        '''
        Checks a lane.
        Returns True if lane contains defense unit.
        '''
        
        lane = list(self.player_buildings[lane_number])
        if (lane[6] > 0):
            return True
        else:
            return False

    def checkTotalEnergyBuildings(self):
        total = 0
        for i in range(8):
            total += self.player_buildings[i].count(3)
        
        return total
    
    def checkAttack(self, lane_number):

        '''
        Checks a lane.
        Returns True if lane contains attack unit.
        '''
        
        lane = list(self.opponent_buildings[lane_number])
        if (lane.count(1) > 0):
            return True
        else:
            return False

        
    def checkMyAttack(self, lane_number):

        '''
        Checks a lane.
        Returns True if lane contains attack unit.
        '''
        
        lane = list(self.player_buildings[lane_number])
        if (lane.count(1) > 0):
            return True
        else:
            return False

    def getUnOccupied(self,lane):
        '''
        Returns index of all unoccupied cells in a lane
        '''
        indexes = []
        for i in range(len(lane)):
            if lane[i] == 0 :
                indexes.append(i)
        
        return indexes
                

    def openEnergyCell(self):
        for col in range(2):
            for row in range(6):
                if self.player_buildings[col][row] == 0:
                    return row,col

    def openAttackCell(self):
        for col in reversed(range(2,8)):
            for row in range(5,-1,-1):
                if self.player_buildings[col][row] == 0:
                    return row,col


    def generateAction(self):
        x,y,building = 0,0,0
        
        col, t = self.shouldDefend()

        if t == 0:
            x,y,building = 0,col,1
        elif t == 1:
            x,y,building = 7,col,0
        elif t == 2:
            x,y,building = 6,col,0
        else:
            if self.checkTotalEnergyBuildings() < 9 and self.energy >= 20:
                x,y = self.openEnergyCell()
                building = 2
            elif self.energy >= 30:
                x,y = self.openAttackCell()
                building = 1
            else:
                self.writeDoNothing()
                return ''

        self.writeCommand(x,y,building)
        return x,y,building
    
    def writeCommand(self,x,y,building):
        '''
        command in form : x,y,building_type
        '''
        outfl = open('command.txt','w')
        outfl.write('{},{},{}'.format(str(x),str(y),str(building)))
        outfl.close()
        # history = open('history.txt', 'a')
        # history.write('{},{},{}\n'.format(str(x),str(y),str(building)))
        # history.close()
        return None

    def writeDoNothing(self):
        '''
        command in form : x,y,building_type
        '''
        outfl = open('command.txt','w')
        outfl.write("")
        outfl.close()
        return None

if __name__ == '__main__':
    s = StarterBot('state.json')
    s.generateAction()
