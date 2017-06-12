#include <iostream>
#include <vector>

using namespace std;

int problem2(vector<int> &A)
{
	int len = 0;
	vector<bool> visited(A.size(), false);
	for(int cur = 0; A[cur] != -1; ++len, cur = A[cur]) {
		if (cur >= A.size() || cur < 0) break; // out of range error!
		if (visited[cur] == true) break; // circular
		visited[cur] = true;
	}
	return len;
}

int main(void)
{
	vector<int> testcase = {1, 4, -1, 3, 2};
	printf("answer: %d\n", problem2(testcase));
}