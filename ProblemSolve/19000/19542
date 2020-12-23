#include<iostream>
#include<vector>
#include<algorithm>
#include<cstring>
using namespace std;

vector<int> g[100'005];
bool visit[100'005];
int dis[100'005];
int cou;
int N, S, D;

int dfs(int node) {
	int MaxDis = 0;
	visit[node] = true;
	for (int next : g[node]) {
		if (!visit[next]) {
			MaxDis = max(dfs(next) + 1, MaxDis);
		}
	}
	dis[node] = MaxDis;
	return dis[node];
}

void search(int node) {
	visit[node] = true;
	for (int next : g[node]) {
		if (!visit[next]) {
			if (dis[next] >= D) {
				cou++;
				search(next);
				cou++;
			}
		}
	}
}

int main() {
	cin >> N >> S >> D;
	for (int i = 0; i < N - 1; i++) {
		int x, y; cin >> x >> y;
		g[x].push_back(y);
		g[y].push_back(x);
	}
	dfs(S);
	memset(visit, false, sizeof(bool) * 100'004);
	search(S);
	cout << cou;
}
