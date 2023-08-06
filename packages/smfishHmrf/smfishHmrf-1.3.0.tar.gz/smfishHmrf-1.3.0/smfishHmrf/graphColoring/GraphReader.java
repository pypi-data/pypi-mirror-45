
import java.util.*;
import java.io.*;

/**
 * Read the graph from Constants.FILE
 * See the following URLs for instances:
 * http://www.nlsde.buaa.edu.cn/~kexu/benchmarks/graph-benchmarks.htm
 * http://mat.gsia.cmu.edu/COLOR/instances.html
 * 
 * @author Shalin Shah
 * Email: shah.shalin@gmail.com
 */
public class GraphReader {
    
    /** Creates a new instance of GraphReader */
    public GraphReader() {
    }
 
    public static Graph readGraph() throws Exception
    {
        BufferedReader reader = new BufferedReader(new FileReader(new File(Constants.FILE)));
        String line = reader.readLine();
        while(line.charAt(0) == 'c')
        {
            line = reader.readLine();
        }
        if(line.charAt(0) != 'p')
        {
            System.out.println("Input File Format Not Understood.");
            System.exit(1);
        }
        
        StringTokenizer token = new StringTokenizer(line, " ");
        token.nextToken();
        token.nextToken();
        Constants.NUMBER_NODES = Integer.parseInt(token.nextToken().trim());
        Graph graph = new Graph();
        line = reader.readLine();
        while(line != null)
        {
            token = new StringTokenizer(line, " ");
            token.nextToken();
            int sv = Integer.parseInt(token.nextToken().trim());
            int ev = Integer.parseInt(token.nextToken().trim());
            sv--;
            ev--;
            graph.addEdge(sv, ev);
            line = reader.readLine();
        }
        
        return graph;
    }

    public static Graph readGraph(String file) throws Exception
    {
		Vector<String> edges = new Vector<String>();
		Map<String,Integer> mm = new HashMap<String,Integer>();
		Map<Integer,String> mm_rev = new HashMap<Integer,String>();
		BufferedReader in = null;
		int c = 0;
		try{
			in = new BufferedReader(new FileReader(file));
			String s = null;
			while((s=in.readLine())!=null){
				edges.add(s);
				StringTokenizer st = new StringTokenizer(s, " ");
				String v1 = st.nextToken();
				String v2 = st.nextToken();
				if(!mm.containsKey(v1)){
					mm.put(v1, c);
					mm_rev.put(c, v1);
					System.out.println(v1 + ": " + c);
					c++;
				}
				if(!mm.containsKey(v2)){
					mm.put(v2, c);
					mm_rev.put(c, v2);
					System.out.println(v2 + ": " + c);
					c++;
				}
			}
		}catch(Exception e){

		}finally{
			if(in!=null) in.close();
		}
		//System.out.println(mm);

		int numV = mm.size();
		Constants.NUMBER_NODES = numV;
		/*
		int graph[][] = new int[numV][numV];
		for(int i=0; i<numV; i++){
			for(int j=0; j<numV; j++){
				graph[i][j] = 0;
			}
		}

		System.out.println(numV);
		*/
		Graph graph = new Graph();
		graph.mStrInt = mm;
		graph.mIntStr = mm_rev;
		for(String e: edges){
			StringTokenizer st = new StringTokenizer(e, " ");
			String v1 = st.nextToken();
			String v2 = st.nextToken();
			int i1 = mm.get(v1);
			int i2 = mm.get(v2);
			//graph[i1][i2] = 1;
			//graph[i2][i1] = 1;
			graph.addEdge(i1, i2);
			
		}
		/*
        BufferedReader reader = new BufferedReader(new FileReader(new File(file)));
        String line = reader.readLine();
        while(line.charAt(0) == 'c')
        {
            line = reader.readLine();
        }
        if(line.charAt(0) != 'p')
        {
            System.out.println("Input File Format Not Understood.");
            System.exit(1);
        }
        
        StringTokenizer token = new StringTokenizer(line, " ");
        token.nextToken();
        token.nextToken();
        Constants.NUMBER_NODES = Integer.parseInt(token.nextToken().trim());
        Graph graph = new Graph();
        line = reader.readLine();
        while(line != null)
        {
            token = new StringTokenizer(line, " ");
            token.nextToken();
            int sv = Integer.parseInt(token.nextToken().trim());
            int ev = Integer.parseInt(token.nextToken().trim());
            sv--;
            ev--;
            graph.addEdge(sv, ev);
            line = reader.readLine();
        }
        */
        return graph;
    }
}
