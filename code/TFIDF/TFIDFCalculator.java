package tfidf;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

/**
 * credit: https://gist.github.com/guenodz/d5add59b31114a3a3c66
 */
public class TFIDFCalculator {
	
	//dictionary:
	//kentucky
	//kentucky high
	// kentucky high school
	
    /**
     * @param doc  list of strings
     * @param term String represents a term
     * @return term frequency of term in document
     */
    public double tf(List<String> doc, String term) {
    	Scanner scanner = new Scanner(term); //store term into a scanner. //Kentucky High School
    	String terms = scanner.next(); //first word. //Kentucky
        double result = 0;
        for (String word : doc) { //word in corpus is "Kentucky"
        	
        	scanner = new Scanner(term);
        	while()
        	{
        		
        	}
        	
        	if (word.equalsIgnoreCase(term)) //kentucky
        	{
        		terms = scanner.next();
        	}
            if (term.equalsIgnoreCase(word))
                result++;
        }
        return result / doc.size();
    }

    /**
     * @param docs list of list of strings represents the dataset
     * @param term String represents a term
     * @return the inverse term frequency of term in documents
     */
    public double idf(List<List<String>> docs, String term) {
        double n = 0;
        for (List<String> doc : docs) {
            for (String word : doc) {
                if (term.equalsIgnoreCase(word)) {
                    n++;
                    break;
                }
            }
        }
        return Math.log(docs.size() / n);
    }

    /**
     * @param doc  a text document
     * @param docs all documents
     * @param term term
     * @return the TF-IDF of term
     */
    public double tfIdf(List<String> doc, List<List<String>> docs, String term) {
        return tf(doc, term) * idf(docs, term);

    }

    List<String> doc1;
    List<String> doc2;
    List<String> doc3;
    String doc4Content;
    Scanner scanner;
    static List<String> pickDocument;
    static List<List<String>> documents;
    static String keyword;
    static boolean programRunning = true;
	static Scanner keyboard;
    public static void main(String[] args) {
    	
    	keyboard = new Scanner(System.in);

    	TFIDFCalculator calculator = new TFIDFCalculator();
        calculator.init();
    	
    	while(programRunning)
    	{
    		  		
        dialog();
        double tfidf = calculator.tfIdf(pickDocument, documents, keyword);
        System.out.println("TF-IDF" + "(" + keyword +") = " + tfidf + "\n");
    	}

    }
    
    
    public static void dialog()
    {
    	System.out.println("Enter 1 to check keyword. ");
    	System.out.println("Enter 2 to quit. ");
    	System.out.print(": ");
    	int input = keyboard.nextInt();
    	keyboard.nextLine();
   // 	System.out.println("nxt: " + keyboard.nextLine());
    	if (input == 1)
    	{
    		System.out.println("Enter String: ");
    		System.out.print(": ");
    		keyword = keyboard.nextLine();
    	//  	System.out.println("keyword: " + keyword);
    	}
    	else
    	{
    		programRunning = false;
    	}
    	
    }
    
    public static void run()
    {
    	
    }
    
    
    
    public void init()
    {
    	doc1 = Arrays.asList("Lorem", "ipsum", "dolor", "ipsum", "sit", "ipsum");
        doc2 = Arrays.asList("Vituperata", "incorrupte", "at", "ipsum", "pro", "quo");
        doc3 = Arrays.asList("Has", "persius", "disputationi", "id", "simul");
      
        
        doc4Content = "Two students were killed Tuesday and 18 other people were wounded "
        		+ "when a 15-year-old boy armed with a handgun opened fire inside a Kentucky high school, "
        		+ "the authorities said. Terrified students ditched their backpacks and scrambled to "
        		+ "get away, and within minutes of the shots' having been fired, sheriff's deputies "
        		+ "were at Marshall County High School in Benton, where they disarmed the student and took "
        		+ "him into custody, officials said. But it was too late to save Bailey Nicole Holt, 15, "
        		+ "who died at the scene, and Preston Ryan Cope, 15, who died later at a trauma center, "
        		+ "Kentucky State Police Commissioner Richard Sanders said early Tuesday night. "
        		+ "Sixteen of the wounded were injured by gunfire and the four others were hurt while trying to "
        		+ "escape, state police said Tuesday night, revising Sanders' earlier report that 14 people were "
        		+ "shot. Three of the victims were listed in critical condition Tuesday night at "
        		+ "Vanderbilt University Medical Center in Knoxville, Tennessee.  In addition to those family "
        		+ "members that have lost loved ones, that have had loved ones injured or hurt or traumatized, "
        		+ "we pray for these people,  Sanders said. Authorities declined to identify the suspect or discuss "
        		+ "a possible motive, but Sanders said he would likely face two counts of murder and  numerous  "
        		+ "counts of attempted murder.The FBI and the federal Bureau of Alcohol, Tobacco, Firearms and "
        		+ "Explosives also joined the investigation. The small town was in shock as teachers and "
        		+ "counselors tried to calm terrified students who described the chaos in the classrooms "
        		+ "when the bullets started flying at 7:57 a.m. (8:57 a.m. ET), shortly after the shooter "
        		+ "entered the school's common area, according to Sanders. Two minutes later, dispatchers "
        		+ "got the first 911 call, he said, and police were on scene by 8:06 a.m. The suspect was "
        		+ "taken into custody almost immediately by the first officer on the scene, he said.  They "
        		+ "were busting down the gates and fences just to get out,  Shea Thompson, whose teenage "
        		+ "siblings were inside the school when the shooting started, told NBC News. Greg Rodgers, "
        		+ "17, a junior, said that when he arrived at school, he saw students racing out of the building. "
        		+ " I pulled off to the side of the road because everyone was running to the main road,  "
        		+ "Greg said.  I asked my friend what was going on, and he told me that there was a school "
        		+ "shooting. I was shocked. He said that someone had just shot up the school.  Greg said the "
        		+ "suspect opened fire as students were heading to classes.  I'm distraught from all of it. "
        		+ "I couldn't really focus driving home,  he said.  I was shaking a lot driving back to my "
        		+ "house. I'm still shaking. ";
       doc4Content = doc4Content.replaceAll("[.]", "");
       doc4Content = doc4Content.replaceAll("[,]", "");
       
       scanner = new Scanner(doc4Content);
       
       pickDocument = new ArrayList<String>();
       while (scanner.hasNext()) {
    	   pickDocument.add(scanner.next());
       }
        
       documents = Arrays.asList(doc1, doc2, doc3, pickDocument);

    }


}