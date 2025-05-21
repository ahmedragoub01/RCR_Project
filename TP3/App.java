package defaultlogique;


import java.io.IOException;
import org.tweetyproject.commons.ParserException;
import org.tweetyproject.logics.ml.reasoner.SimpleMlReasoner;
import org.tweetyproject.logics.ml.syntax.MlBeliefSet;
import org.tweetyproject.logics.fol.syntax.FolFormula;
import org.tweetyproject.logics.ml.parser.MlParser;


public class App {
    public static void main(String[] args) throws ParserException, IOException {
        MlParser parser = new MlParser();
        MlBeliefSet b1 = parser.parseBeliefBaseFromFile("src/main/resources/examplebeliefbase2.mlogic");
        FolFormula f1 = (FolFormula) parser.parseFormula("<>(A&&B)");
        System.out.println("Parsed formula:" + f1);


        parser = new MlParser();
        MlBeliefSet b2 = parser.parseBeliefBase("Animal = {penguin,eagle} \n type(Flies(Animal)) \n (Flies(eagle))");
        FolFormula f2 = (FolFormula) parser.parseFormula("(Flies(penguin)) || (!(Flies(penguin)))");
        System.out.println("Parsed belief base:" + b2);
        System.out.println("Parsed formula:" + f2);


        parser = new MlParser();
        MlBeliefSet b3 = parser.parseBeliefBaseFromFile("src/main/resources/examplebeliefbase.mlogic");
        System.out.println("Parsed belief base:" + b3 + "\nSignature of belief base:" + b3.getMinimalSignature());


        SimpleMlReasoner reasoner = new SimpleMlReasoner();
        System.out.println("Answer to query: " + reasoner.query(b1, f1));
        System.out.println("Answer to query: " + reasoner.query(b2, f2));
    }
}
