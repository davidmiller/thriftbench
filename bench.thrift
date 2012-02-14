//
// Simple thrift interface for benchmarking purposes
//

service Bencher{
    string ping()
    list<i32> sortset(1: list<i32> unsorted)
}