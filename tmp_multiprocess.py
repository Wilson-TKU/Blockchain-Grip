def kill_child_processes(parent_pid, sig=signal.SIGTERM):
    try:
        parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
        return
    children = parent.children(recursive=True)
    for process in children:
        process.send_signal(sig)
def worker(i, quit, foundit, return_dict):
    print ("%d started" % i)
    while not quit.is_set():
        x = random.random()
        if x > 0.7:
            print ('%d found %g' % (i, x))
            return_dict[i] = x
            foundit.set()
            break
        sleep(0.1)
    print ("%d is done" % i)


 # result_new_proof = 0
    # result_hash_operation = 0
    # print(result_new_proof)
    # print(result_hash_operation)
    

    # start = time()    
    # futures = []
    # # used to create the partitions
    # with ProcessPoolExecutor(core_num) as pool:
    #     for _ in range(core_num):
    #         # run 4 tasks with a partition, but only *one* solution is needed
    #         futures.append(pool.submit(blockchain.proof_of_work, previous_proof))

    #     ### New Code: Start ### 
    #     for f in as_completed(futures):
    #         print(f.result())
    #         if f.result():
    #             print('break')
    #             break

    #     for f in futures:
    #         print(f, 'running?',f.running())
    #         if f.running():
    #             f.cancel()
    #             print('Cancelled? ',f.cancelled())

    #     print('New Instruction Ended at = ', time()-start )
    # print('Total Compute Time = ', time()-start )

    #------------------------
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     results = [executor.submit(blockchain.proof_of_work, previous_proof) for _ in range(core_num)]
    #     # print(results)
    #     for f in concurrent.futures.as_completed(results):
    #         print(f.result())
    #         proof, proof_ans = f.result()
    #         # executor.shutdown()
    #         f.cancel()
    #         executor.shutdown()
    #------------------------
    # process = []
    # for i in range(core_num):
    #     process.append(multiprocessing.Process(target=blockchain.proof_of_work, args=[previous_proof]))
    #     process[i].start()
    # # for i in range(core_num):
    # #     print(f'join:{i}')
    # #     process[i].join()
    # # while(result_new_proof == 0):
    # #     continue
    # for i in range(core_num):
    #     print(process[i].terminate())


    # proof, proof_ans = blockchain.proof_of_work(previous_proof)
    # print(type(return_dict))
    # print(return_dict.values)