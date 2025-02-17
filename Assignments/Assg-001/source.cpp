#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <random>

using namespace std;

class CNICHashMap {
private:
    string cnic_prefix;
    int table_size;
    vector<vector<string>> table;

    uint64_t custom_hash(const string& suffix) const
    {
        uint64_t hash = 0;
        for (int i = 0; i < suffix.length(); i++)
        {
            hash = (hash * 31) + (suffix[i] - '0');
        }
        return hash;
    }

    int hash(const string& cnic) const
    {
        if (cnic.substr(0, cnic_prefix.size()) != cnic_prefix) return -1;

        for (int i = 0; i < cnic.length(); i++)
        {
            char c = cnic[i];
            if (c < '0' || c > '9') return -1;
        }

        string suffix = cnic.substr(cnic_prefix.size(), 9);
        return custom_hash(suffix) % table_size;
    }

public:
    CNICHashMap(const string& prefix, int size) : cnic_prefix(prefix), table_size(size), table(size) {}

    void insert(const string& cnic)
    {
        if (cnic.length() != 13)
        {
            cout << "Invalid CNIC length: " << cnic << endl;
            return;
        }

        int index = hash(cnic);
        if (index < 0 || index >= table_size)
        {
            cout << "Invalid CNIC for this hashmap: " << cnic << endl;
            return;
        }

        table[index].push_back(cnic);
    }

    bool contains(const string& cnic) const
    {
        int index = hash(cnic);
        if (index < 0 || index >= table_size) return false;

        for (size_t i = 0; i < table[index].size(); i++)
        {
            if (table[index][i] == cnic)
            {
                return true;
            } 
        }
        return false;
    }

    void getCollisionStats(int& avg, int& max) const
    {
        int total = 0;
        max = 0;
        
        for (int i = 0; i < table_size; i++)
        {
            int collisions;
            if (table[i].size() > 0)
            {
                collisions = table[i].size() - 1;
            } 
            else
            {
                collisions = 0;
            }
            
            total += collisions;
            
            if (collisions > max) {
                max = collisions;
            }
        }

        if (table_size > 0)
        {
            avg = total / table_size;
        }
        else
        {
            avg = 0;
        }
    }
};

void generateCNICs(const string& prefix, int count, const string& filename)
{
    ofstream file(filename);
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis(0, 9);

    int s = 13 - prefix.size(); // 13 is CNIC length and subtract 
    for (int i = 0; i < count; ++i) {
        string cnic = prefix;
        for (int j = 0; j < s; ++j) {
            cnic += to_string(dis(gen));
        }
        file << cnic << '\n';
    }
    file.close();
}

int main() {
    const string prefix = "3520";
    const int size = 1000;
    const string filename = "cnic-test-data.txt";


    // generateCNICs is function that just create a file which contains demo CNIC's that starts with given prefix (3520) and we
    // give him a count and then the function creates count CNIC's
    int count = 5000;
    generateCNICs(prefix, count, filename);
    CNICHashMap hm(prefix, size);

    ifstream file(filename);
    string cnic;
    vector<string> searchcnic;
    while (getline(file, cnic)) {
        hm.insert(cnic);
        searchcnic.push_back(cnic);
    }


    for(int i=0;i<searchcnic.size();i++)
    {
        if(!hm.contains(searchcnic[i]))
        {
            cout<<"Not found why It does not found there seem to be an issue "<<endl;
        }
        else
        {
            cout<<searchcnic[i]<<"  ->   Found"<<endl;
        }
    }

    //Some not found examples 

    vector<string>notfound;
    notfound.push_back("352025318349");
    notfound.push_back("352015218249");
    notfound.push_back("352025216359");

    for(int i=0;i<notfound.size();i++)
    {
        if(hm.contains(notfound[i]))
        {
            cout<<"found why It does found there seem to be an issue "<<endl;
        }
        else
        {
            cout<<notfound[i]<<"  ->   Not Found"<<endl;
        }
    }

    int avg, max;
    hm.getCollisionStats(avg, max);
    cout << "Average collisions: " << avg << "\nMax collisions: " << max << endl;

    return 0;
}