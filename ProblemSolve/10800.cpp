#include<iostream>
#include<vector>
#include<utility>
using namespace std;

typedef pair<int,int> P;

int ans[200'005];
int cnt[200'005];
int sum=0;
vector<P> arr[2'005];

int main(){
    int N; cin>>N;
    for(int n=0;n<N;n++){
        int a,b;//color, size
        cin>>a>>b;
        arr[b].push_back(P(a,n));
    }

    for(int i=0;i<arr[1].size();i++){
        cnt[arr[1][i].first] += 1;
        sum++;
    }
    for(int size=2;size<=2'000;size++){
        for(int i=0;i<arr[size].size();i++){
            ans[arr[size][i].second] = sum-cnt[arr[size][i].first];
        }
        for(int i=0;i<arr[size].size();i++){
            cnt[arr[size][i].first] += size;
            sum+=size;
        }
    }
    for(int i=0;i<N;i++){
        cout<<ans[i]<<"\n";
    }
}
