package test.java.demo;

import org.junit.Test;
import static org.junit.Assert.*;
import main.java.demo.Year;

public class YearTest {
    
    @Test
    public void shouldReturnMeh() {
        Year y = new Year(1);
        assertTrue(y.review().equals("Meh"));
    }
}
