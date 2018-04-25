#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <ctime>
#include <vector>
#include <queue>
#include<iostream>
#include<cstring>
#include<io.h>
using namespace std;

struct Edge {
	int from, to;//                                         
	double cap, flow;
};

template<int MAXSIZE>
struct Dinic {
	int n, m, s, t;
	vector<Edge> edges;    // 边数的两倍
	vector<int> G[MAXSIZE];   // 邻接表，G[i][j]表示节点i的第j条边在边集合 edges 中的序号
	bool vis[MAXSIZE];         // BFS使用
	int d[MAXSIZE];           // 从起点到i的距离
	int cur[MAXSIZE];        // 当前弧指针

	void ClearAll(int n) {
		for (int i = 0; i < n; i++) G[i].clear();
		edges.clear();
		memset(vis, 0, sizeof(vis));
		memset(d, 0, sizeof(d));
		memset(cur, 0, sizeof(cur));

	}

	void Reserve(int _n)
	{
		g.n = _n;
	}

	void ClearFlow() {
		for (int i = 0; i < edges.size(); i++) edges[i].flow = 0;
	}

	void AddEdge(int from, int to, double cap) {
		Edge arc1 = { from,to,cap,0 };
		Edge arc2 = { to, from,0,0 };
		edges.push_back(arc1);
		edges.push_back(arc2);
		m = edges.size();
		G[from].push_back(m - 2);
		G[to].push_back(m - 1);
	}

	void PrintG() {
		for (int i = 0; i < MAXSIZE; i++)
		{
			printf("%i: ", i );
			int size_i = G[i].size();
			for (int j = 0; j < size_i; j++)
			{
				printf("%i  ", G[i][j]);
			}
			printf("\n");
		}
	}

	void PrintGraph() {
		int count = 0;
		for (int i = 0; i < edges.size(); i++)
		{
			printf("(%i,%i): %.1f, %.1f  ", edges[i].from, edges[i].to, edges[i].cap, edges[i].flow);
			count++;
			if (count==4)
			{
				printf("\n");
				count = 0;
			}
		}
		printf("\n");
		printf("\n");
	}

	bool BFS() {
		memset(vis, 0, sizeof(vis));
		queue<int> Q;
		Q.push(s);
		vis[s] = 1;
		d[s] = 0;
		while (!Q.empty()) {
			int x = Q.front(); Q.pop();
			for (int i = 0; i <  G[x].size(); i++) {
				Edge& e = edges[G[x][i]];
				if (!vis[e.to] && e.cap - e.flow > 0) {
					vis[e.to] = 1;
					d[e.to] = d[x] + 1;
					Q.push(e.to);
				}
			}
		}
		return vis[t];
	}

	double DFS(int x, double a)
	{
		if (x == t || a <= 0) return a;
		double flow = 0;
		double f = 0;
		for (int& i = cur[x]; i < G[x].size(); i++)
		{
			Edge& e = edges[G[x][i]];
			if (d[x] + 1 == d[e.to] && (f = DFS(e.to, min(a, e.cap - e.flow))) > 0) {
				e.flow += f;
				edges[G[x][i] ^ 1].flow -= f; //^ ：按位异或运算符 参与运算的两个值，如果两个相应位相同，则结果为0，否则为1。即：0 ^ 0 = 0， 1 ^ 0 = 1， 0 ^ 1 = 1， 1 ^ 1 = 0
				flow += f;
				a -= f;
				if (a == 0) break;
			}
		}
		return flow;
	}

	double Maxflow(int s, int t) {
		this->s = s; this->t = t;
		double flow = 0;
		while (BFS()) {
			memset(cur, 0, sizeof(cur));
			flow += DFS(s, INF);
			PrintGraph();
		}
		return flow;
	}

	vector<int> Mincut(int source) { // call this after maxflow
		vector<int> SourceNodes;
		for (int i = 0; i < edges.size(); i++)
		{
			Edge& e = edges[i];
			if (vis[e.from] && vis[e.to] && e.cap>0)
			{
				SourceNodes.push_back(e.from);
			}
		}
		sort(SourceNodes.begin(), SourceNodes.end());
		SourceNodes.erase(unique(SourceNodes.begin(), SourceNodes.end()), SourceNodes.end());
		return SourceNodes;
	}
};

const double INF = 10000;

int main()
{
	Dinic<8> graph;

	graph.AddEdge(0, 1, 10);
	graph.AddEdge(0, 2, 5);
	graph.AddEdge(0, 3, 15);
	graph.AddEdge(1, 2, 4);
	graph.AddEdge(1, 4, 9);
	graph.AddEdge(1, 5, 15);
	graph.AddEdge(2, 3, 4);
	graph.AddEdge(2, 5, 8);
	graph.AddEdge(3, 6, 30);
	graph.AddEdge(4, 5, 15);
	graph.AddEdge(4, 7, 10);
	graph.AddEdge(5, 6, 15);
	graph.AddEdge(5, 7, 10);
	graph.AddEdge(6, 7, 10);
	graph.AddEdge(6, 2, 6);//共15条边

	graph.PrintG();
	graph.PrintGraph();
	double max_f = graph.Maxflow(0, 4);
	printf("从 %i - %i 的最大流量为： %1.2f \n", 0, 7, max_f);
	vector<int> vecS = graph.Mincut(0);
	printf("与 %i 相连的割集包括： ", 0);
	for (int i = 0; i < vecS.size(); i++)
	{
		printf("%i  ", vecS[i]);
	}
	printf("\n");
	system("pause");


}
