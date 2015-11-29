import sys
import math

# Save humans, destroy zombies!


def getDistance(p1, p2):
	return math.sqrt(math.pow((p1[0] - p2[0]), 2) + math.pow((p1[1] - p2[1]), 2))


def getZombiesinRange(playerpos, zombiepos):
	shootrange = 2000
	zinrange = set()
	for zombie in zombiepos:
		if getDistance(zombie[1:], playerpos) <= shootrange:
			zinrange.add(zombie[0])
	return zinrange


def getScore(playerpos, humanpos, zombiepos):
	zinrange = getZombiesinRange(playerpos, zombiepos)
	score = getFibNo(len(zinrange)) * len(humanpos) * len(humanpos) * 10
	return score


def getNearestHuman(zombie, humanpos, playerpos):
	dist = float("inf")
	closest = []
	for human in humanpos:
		d = getDistance(human, zombie[1:])
		if d < dist:
			closest = human
			dist = d
	d = getDistance(playerpos, zombie[1:])
	if d < dist:
		closest = playerpos
		dist = d
	return closest


def greedyMove(playerpos, humanpos, zombiepos, depth):
	if depth == 0:
		return ([], 0)
	moves = getValidMoves(playerpos) # gets a list of positions
	best = -1
	bestmove = []
	for move in moves:
		newhumanpos, newzombiepos = makeMove(move, humanpos, zombiepos)
		curscore = getScore(move, humanpos, zombiepos)
		moveseq, score = greedyMove(move, newhumanpos, newzombiepos)
		if (curscore + score) > best:
			best = curscore + score
			bestmove = moveseq.insert(0, move)
	return (bestmove, best)




def makeMove(playerpos, humanpos, zombiepos):
	zinrange = getZombiesinRange(playerpos, zombiepos)
	newzombiepos = []
	newhumanpos = []
	for zombie in zombiepos:
		if zombie[0] not in zinrange:
			for human in humanpos:
				if human[0] == zombie[1] and human[1] == zombie[2]:
					continue
				else:
					newhumanpos.append(human)
	for zombie in zombiepos:
		if zombie[0] not in zinrange:
			newpos = getNearestHuman(zombie, newhumanpos, playerpos)
			newzombiepos.append([zombie[0], newpos[0], newpos[1]])
	return (newhumanpos, newzombiepos)

# game loop
while 1:
	x, y = [int(i) for i in input().split()]
	human_count = int(input())
	for i in range(human_count):
		human_id, human_x, human_y = [int(j) for j in input().split()]
	zombie_count = int(input())
	for i in range(zombie_count):
		zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]

	# Write an action using print
	# To debug: print("Debug messages...", file=sys.stderr)

	# Your destination coordinates
	print("16000 9000")
