package defaultlogique;


import java.io.IOException;
import java.util.ArrayList;
import java.util.List;


import org.tweetyproject.commons.ParserException;
import org.tweetyproject.logics.commons.syntax.Constant;
import org.tweetyproject.logics.commons.syntax.Predicate;
import org.tweetyproject.logics.commons.syntax.Sort;
import org.tweetyproject.logics.fol.parser.FolParser;
import org.tweetyproject.logics.fol.reasoner.FolReasoner;
import org.tweetyproject.logics.fol.reasoner.SimpleFolReasoner;
import org.tweetyproject.logics.fol.syntax.FolBeliefSet;
import org.tweetyproject.logics.fol.syntax.FolFormula;
import org.tweetyproject.logics.fol.syntax.FolSignature;


public class App {
    public static void main(String[] args) throws ParserException, IOException {
        FolSignature sig = new FolSignature(true);


        Sort sortAnimal = new Sort("Animal");
        sig.add(sortAnimal);


        Constant constantPenguin = new Constant("penguin", sortAnimal);
        Constant constantKiwi = new Constant("kiwi", sortAnimal);
        sig.add(constantPenguin, constantKiwi);


        List<Sort> predicateList = new ArrayList<>();
        predicateList.add(sortAnimal);
        Predicate p = new Predicate("Flies", predicateList);


        List<Sort> predicateList2 = new ArrayList<>();
        predicateList2.add(sortAnimal);
        predicateList2.add(sortAnimal);
        Predicate p2 = new Predicate("Knows", predicateList2);


        sig.add(p, p2);
        System.out.println("Signature: " + sig);


        FolParser parser = new FolParser();
        parser.setSignature(sig);


        FolBeliefSet bs = new FolBeliefSet();
        bs.add(
            (FolFormula) parser.parseFormula("!Flies(kiwi)"),
            (FolFormula) parser.parseFormula("Flies(penguin)"),
            (FolFormula) parser.parseFormula("!Knows(penguin,kiwi)"),
            (FolFormula) parser.parseFormula("/==(penguin,kiwi)"),
            (FolFormula) parser.parseFormula("kiwi == kiwi")
        );


        System.out.println("\nParsed BeliefBase: " + bs);


        FolSignature sigLarger = bs.getSignature();
        sigLarger.add(new Constant("archaeopteryx", sortAnimal));
        bs.setSignature(sigLarger);


        System.out.println(bs);
        System.out.println("Minimal signature: " + bs.getMinimalSignature());


        FolReasoner.setDefaultReasoner(new SimpleFolReasoner());
        FolReasoner prover = FolReasoner.getDefaultReasoner();


        System.out.println("ANSWER 1: " + prover.query(bs, (FolFormula) parser.parseFormula("Flies(kiwi)")));
        System.out.println("ANSWER 2: " + prover.query(bs, (FolFormula) parser.parseFormula("forall X: (exists Y: (Flies(X) && Flies(Y) && X/==Y))")));
        System.out.println("ANSWER 3: " + prover.query(bs, (FolFormula) parser.parseFormula("kiwi == kiwi")));
        System.out.println("ANSWER 4: " + prover.query(bs, (FolFormula) parser.parseFormula("kiwi /== kiwi")));
        System.out.println("ANSWER 5: " + prover.query(bs, (FolFormula) parser.parseFormula("penguin /== kiwi")));
    }
}
