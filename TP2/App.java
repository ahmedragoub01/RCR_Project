package defaultlogique;


import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;


import org.tweetyproject.logics.fol.parser.FolParser;
import org.tweetyproject.logics.fol.reasoner.FolReasoner;
import org.tweetyproject.logics.fol.syntax.FolBeliefSet;
import org.tweetyproject.logics.fol.syntax.FolFormula;
import org.tweetyproject.logics.fol.syntax.FolSignature;
import org.tweetyproject.logics.fol.writer.StandardFolWriter;
import org.tweetyproject.commons.ParserException;
import org.tweetyproject.commons.Signature;
import org.tweetyproject.logics.commons.syntax.Constant;
import org.tweetyproject.logics.commons.syntax.Predicate;
import org.tweetyproject.logics.commons.syntax.Sort;
import org.tweetyproject.logics.commons.syntax.Functor;


public class App {
    public static void main(String[] args) throws ParserException, IOException {
        String filename = "src\\main\\resources\\test.fol";


        FolSignature sig = new FolSignature();
        Sort animal = new Sort("animal");
        sig.add(animal);
        Constant anna = new Constant("anna", animal);
        sig.add(anna);
        Constant bob = new Constant("bob", animal);
        sig.add(bob);
        Sort plant = new Sort("plant");
        sig.add(plant);
        Constant emma = new Constant("emma", plant);
        sig.add(emma);


        List<Sort> l = new ArrayList<Sort>();
        l.add(animal);
        Predicate flies = new Predicate("flies", l);
        sig.add(flies);


        l = new ArrayList<Sort>();
        l.add(animal);
        l.add(plant);
        Predicate eats = new Predicate("eats", l);
        sig.add(eats);


        l = new ArrayList<Sort>();
        l.add(animal);
        Functor fatherOf = new Functor("fatherOf", l, animal);
        sig.add(fatherOf);


        FolBeliefSet b = new FolBeliefSet();
        b.setSignature(sig);
        FolParser parser = new FolParser();
        parser.setSignature(sig);


        b.add(parser.parseFormula("forall X:(flies(X) => (exists Y:(eats(X,Y))))"));
        b.add(parser.parseFormula("forall X:(flies(X) => flies(fatherOf(X)))"));
        b.add(parser.parseFormula("flies(anna)"));
        b.add(parser.parseFormula("eats(bob,emma)"));


        System.out.println(b);


        StandardFolWriter writer = new StandardFolWriter(new FileWriter(filename));
        writer.printBase(b);
        writer.close();


        parser = new FolParser();
        System.out.println(parser.parseBeliefBaseFromFile(filename));
    }
}
