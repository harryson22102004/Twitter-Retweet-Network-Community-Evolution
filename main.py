import networkx as nx, random
from collections import defaultdict
 
def build_retweet_graph(n_users=100, n_tweets=500):
    G=nx.DiGraph()
    users=[f"u{i}" for i in range(n_users)]
    for _ in range(n_tweets):
        author=random.choice(users)
        retweeters=random.sample(users,k=random.randint(1,5))
        for r in retweeters:
            if r!=author:
                if G.has_edge(r,author): G[r][author]['weight']+=1
                else: G.add_edge(r,author,weight=1)
    return G
 
def temporal_community_detection(G_list):
    from networkx.algorithms.community import greedy_modularity_communities
    results=[]
    for t,G in enumerate(G_list):
        ug=G.to_undirected()
        if ug.number_of_edges()>0:
            comms=list(greedy_modularity_communities(ug))
            results.append({'t':t,'n_communities':len(comms),
                             'sizes':[len(c) for c in comms],
                             'modularity':nx.algorithms.community.modularity(ug,comms)})
    return results
 
def detect_influential_users(G):
    pr=nx.pagerank(G,alpha=0.85)
    return sorted(pr,key=pr.get,reverse=True)[:5], pr
 
snapshots=[build_retweet_graph(50,200) for _ in range(3)]
evol=temporal_community_detection(snapshots)
for e in evol: print(f"T={e['t']}: {e['n_communities']} communities, mod={e['modularity']:.3f}")
inf,pr=detect_influential_users(snapshots[-1])
print(f"Top influencers: {inf}")
