/*
Implement an autocomplete system. Given a list of strings and their corresponding usage frequencies, implement a class with the following features:
1. add(word: str, freq: int): Adds a new word with its frequency. If the word already exists, update its frequency by to the given value.
2. top_k(prefix: str, k: int) -> List[str]: Returns the top k most frequent words that start with the given prefix. In case of a tie in frequency, sort lexicographically.
Constraints:
* word contains only lowercase English letters.
* 1 <= word.length <= 100
* 1 <= freq <= 10^5
* 1 <= k <= 100
* Up to 10^5 total calls to add() and top_k() combined.
*/

/*

   Trie: go up to finding that prefix. From there, whichever words are present - topK
   // maintaining min heap: if size clash, choose lexicographically.
   
   creating min heap: O(nlogK) picking O(K): total O(NlogK + K)
   
   Trie:
      at each node min_heap: off all words which pass through it. 
      top_k: O(prefix len + K): O(1) because upper limit fixed
      
      For existing elem:
        - first remove the element from PQ ... (pop all till elem, update elem put everything back)
        - then insert with new freq.
  
*/

#include <iostream>
#include <map>
#include <queue>
#include <stack>
#include <string>
#include <vector>
#include <set>
using std::vector;
using std::cout;
using std::endl;
using std::pair;
using std::priority_queue;
using std::string;
using std::stack;
using std::map;


struct LessFreqFirst {
    bool operator()(const pair<string, int>& a, const pair<string, int>& b) {
        if (a.second < b.second) return true;
        else if (a.second > b.second) return false;
        else  { // (a.second == b.second)
            return a.first > b.first; 
            // lexicographical order. we want later string true
        }
    }
};

class TrieNode { // One node
public:
    void insert(const string& orig_str, int freq) {
        insert(orig_str, orig_str, freq);
    }
    
    void print() {
        // bfs
        
    }
    
    vector<string> topK(const string& prefix, int n) {
         vector<string>  result;
        if (prefix.empty()) {
            return result;  // empty
        }
        if (prefix.size() == 1) {
            //topK from pq
           stack<pair<string, int>> buffer;
           for (int i = 0; (i < n) && !word_to_freq_max_heap.empty(); i++) {
               result.push_back(word_to_freq_max_heap.top().first);
               buffer.push(word_to_freq_max_heap.top());
               word_to_freq_max_heap.pop();
           }
           while (buffer.size()) {
               word_to_freq_max_heap.push(buffer.top());
               buffer.pop();
           }
           return result;
        }        

        // go up to that node and return topK
        char first_char = prefix[0];
        if (children.find(first_char) == children.end()) {
            return result;  // empty
        }
        return children[first_char]->topK(prefix.substr(1), n);
    }
    

private:
    std::map<char, TrieNode*> children;  // no null or empty.
    bool is_word_end = false;
    char parent = '\0';
    
    // At each node we remember word:freq map of words passing through it.
    std::priority_queue<pair<string, int>, vector<pair<string, int>>, LessFreqFirst> word_to_freq_max_heap;
    std::set<string> words_witnessed; // or else each time we have to pop words from queue and again put back. note that if it is already present, you have to do O(n) anyways to update it.
    
    void insert(const string& orig_str, const string& remaining_str, int freq) {
     printf("\n[%c].insert(%s, %s, %d). as of now word_to_freq_max_heap %zu", parent, orig_str.c_str(), remaining_str.c_str(), freq, word_to_freq_max_heap.size());
     if (words_witnessed.size() != word_to_freq_max_heap.size()) {
         printf("\nError");
     }
     
     // orig_str reached here, so first record its frequency.
     // if orig_str already present, increase it.
     {
         if (words_witnessed.find(orig_str) == words_witnessed.end()) {
             words_witnessed.insert(orig_str);
             word_to_freq_max_heap.push(pair<string, int>(orig_str, freq));
         } else { // already present
           stack<pair<string, int>> existing_entries;
           while(word_to_freq_max_heap.top().first != orig_str) {
               existing_entries.push(word_to_freq_max_heap.top());
               word_to_freq_max_heap.pop();
           }
           auto entry = word_to_freq_max_heap.top();
           word_to_freq_max_heap.pop();
           entry.second += freq;
           word_to_freq_max_heap.push(entry);
           while (existing_entries.size()) {
               word_to_freq_max_heap.push(existing_entries.top());
               existing_entries.pop();
           }
         }
     }

     // child node or end_of_word
     if (remaining_str.empty()) {
         is_word_end = true;
     } else {
         char first_char = remaining_str[0];
         TrieNode* child = NULL;
         if (children.find(first_char) == children.end()) {
             child = new TrieNode();
             child->parent = first_char;
             children[first_char] = child;
         } else {
             child = children[first_char];
         }
        child->insert(orig_str, remaining_str.substr(1), freq);
     }
     
     printf("\n[%c].insert(%s, %s, %d) - my pq size = %zu, my children size = %zu", parent, orig_str.c_str(), remaining_str.c_str(), freq, word_to_freq_max_heap.size(), children.size());     
    }
    
};

int main() {
    cout << "Making TrieNode" << endl;
    TrieNode* trie = new TrieNode();
    trie->insert("karan1", 1);
    trie->insert("karan2", 2);
    trie->insert("karan3", 3);
    trie->insert("karan4", 4);
    trie->insert("karan5", 5);
    trie->insert("karan6", 6);

    trie->insert("kb9", 9);
    
    auto result = trie->topK("k",4);
    for (string entry : result) {
        cout << "\nresult " << entry << endl;
    }

    return 0;
}

