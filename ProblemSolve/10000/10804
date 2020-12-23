#include<iostream>
#include<vector>
#include<stack>
using namespace std;

int main(){
    int arr[21];
    for(int i=1;i<=20;i++){
        arr[i] = i;
    }

    int a,b;
    for(int i=0;i<10;i++){
        cin>>a>>b;
        stack<int> s;
        for(int j=a;j<=b;j++){
            s.push(arr[j]);
        }
        for(int j=a;j<=b;j++){
            arr[j] = s.top();
            s.pop();
        }
    }

    for(int i=1;i<=20;i++){
        cout<<arr[i]<<" ";
    }
    return 0;
}
