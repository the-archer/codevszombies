import sys
import math

# Save humans, destroy zombies!


def getFibNo(x):
	fib = [0,1,2,4,7,12,20,33,54,88,143,232,376,609,986,1596,2583,4180,6764,10945,17710,28656,46367,75024,121392,196417,317810,514228,832039,1346268,2178308]
	return fib[min(x, 30)]


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


def getValidMoves(playerpos):
	movdist = 1000
	directions = 8
	movelist = [playerpos]
	for deg in range(0, 360, 360//directions):
		x = math.floor(playerpos[0] + math.sin(math.radians(deg))*movdist)
		y = math.floor(playerpos[1] - math.cos(math.radians(deg))*movdist)
		if x < 0:
			x = 0
		if x > 16000:
			x = 16000
		if y < 0:
			y = 0
		if y > 9000:
			y = 9000
		movelist.append([x, y])
	return movelist


def greedyMove(playerpos, humanpos, zombiepos, depth):
	# print(str(depth), file = sys.stderr)
	if depth == 0:
		return ([], 0)
	moves = getValidMoves(playerpos)  # gets a list of positions
	best = -1
	bestmove = []
	# print(moves, file = sys.stderr)
	for move in moves:
		newhumanpos, newzombiepos = makeMove(move, humanpos, zombiepos)
		curscore = getScore(move, humanpos, zombiepos)
		moveseq, score = greedyMove(move, newhumanpos, newzombiepos, depth-1)
		if (curscore + score) > best:
			best = curscore + score
			moveseq.insert(0, move)
			bestmove = moveseq
	print(str(bestmove) + " " + str(best), file = sys.stderr)
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
maxd = 3
movelist = []
while 1:
	humanpos = []
	zombiepos = []
	x, y = [int(i) for i in input().split()]
	human_count = int(input())
	for i in range(human_count):
		human_id, human_x, human_y = [int(j) for j in input().split()]
		humanpos.append([human_x, human_y])
	zombie_count = int(input())
	for i in range(zombie_count):
		zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]
		zombiepos.append([zombie_id, zombie_xnext, zombie_ynext])
	playerpos = [x, y]
	if len(movelist) == 0:
		movelist, score = greedyMove(playerpos, humanpos, zombiepos, maxd)

	# Write an action using print
	# To debug: print("Debug messages...", file=sys.stderr)

	# Your destination coordinates
	print(str(movelist[0][0]) + " " + str(movelist[0][1]))
	movelist.pop(0)
	# print("16000 9000")
