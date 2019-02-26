#include <iostream>
#include <fstream>
#include <string>
#include <vector>
using namespace std;
int main(int argc, char **argv)
{
    if (argc != 3)
        return -1;
    string fileName(argv[1]);
    string nums(argv[2]);
    int credits = stoi(nums);
    //cout<< fileName<<" "<< credits<<endl;

    ifstream infile(fileName);
    std::string line;
    vector< pair<int, string> > myVec;
    while (std::getline(infile, line))
    {

        size_t pos = 0;
        std::string delimiter = ", ";
        pos = line.find(delimiter);
        string itemName = line.substr(0, pos);
        //std::cout << itemName << std::endl;
        line.erase(0, pos + delimiter.length());

        pos = line.find(delimiter);
        string prices = line.substr(0, pos);
        //std::cout << prices <<"end"<< std::endl;

        int price = stoi(prices);

        //cout<< price<<itemName<<endl;
        myVec.push_back(make_pair(price, itemName));
    }

    int left = 0, right = myVec.size() - 1;
    int diff = credits + 1;
    int finalLeft = left, finalRight = right;
    while (left < right)
    {
        int twoSum = myVec[left].first + myVec[right].first;
        if (twoSum <= credits)
        {
            if (credits - twoSum < diff)
            {
                diff = credits - twoSum;
                finalLeft = left;
                finalRight = right;
            }
            left++;
        }
        else
        {
            right--;
        }
    }

    if (diff > credits)
        cout << "Not possible" << endl;
    else
    {
        cout << myVec[finalLeft].first << myVec[finalLeft].second << endl;
        cout << myVec[finalRight].first << myVec[finalRight].second << endl;
    }
    return 0;
}