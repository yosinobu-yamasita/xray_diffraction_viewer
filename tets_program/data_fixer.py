start_dig = 20
end_dig =50
step_dig =0.02

now_dig = start_dig
for i in range(int((end_dig-start_dig)/step_dig)):
    now_dig+=step_dig
    print("i:",i,"renew:",start_dig+(i+1)*step_dig," add:",now_dig)

