dense_clustering.py 실행할 때 --make_cluster를 Ture로 하면 클러스터링 넘버를 추가, 클러스터링 넘버마다 엠베딩이 연결된 df 생성
--make_file을 True로 하면 위의 클러스터링 한 df들을 저장해줌
--make_file을 True로 안해도 클러스터 성능을 체크한 후 한번 더 저장할지 여부 물어봄
데이터가 많으면 hdb, 적으면 db쓰기