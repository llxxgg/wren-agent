import asyncio

PENDING, COMPLETED = "pending", "completed"

class Plan:
	def __init__(self):
		self.nodes = {}
		self._pred = {}
		
	def add_node(self, name, node):
		self.nodes[name] = node
		self._pred.setdefault(name, [])
		
	def add_edge(self, src, dst):
		# dst 增加前置节点
		self._pred.setdefault(dst, []).append(src)
		
	def ready(self, run: Run):
		# 根据运行状态，获取ready节点
		out = []
		for name, node in self.nodes.items():
			if run.states.get(name, PENDING) != PENDING:
				continue
			if all(run.states.get(p) == COMPLETED for p in self._pred[name]):
				out.append(name)
				
		return out
		
class Run:
	def __init__(self):
		self.states = {}
		self.shared = {}
		

class Schedule:
	
	async def drive(self, plan, run):
		run = Run()
		wave = 0
		while True:
			ready = plan.ready(run)
			if not ready:
				break
				
			wave = wave + 1
			print(f"wave {wave}: {ready}")
			
			async def run_node(name):
				value = await plan.nodes[name](run.shared)
				run.shared[name] = value
				run.states[name] = COMPLETED
				
			await asyncio.gather(*[run_node(name) for name in ready])
			
		return run.shared

async def a(shared):
	return "node a done"
async def b(shared):
	return "node a done"
async def c(shared):
	return "node a done"
async def d(shared):
	return "node a done"

if __name__ == "__main__":
	plan = Plan()
	plan.add_node("a", a)
	plan.add_node("b", b)
	plan.add_node("c", c)
	plan.add_node("d", d)
	plan.add_edge("a", "b")
	plan.add_edge("a", "c")
	plan.add_edge("b", "d")
	plan.add_edge("c", "d")
	
	run = Run()
	
	schedule = Schedule()
	final = asyncio.run(schedule.drive(plan, run))
	print("final shared:", final)


