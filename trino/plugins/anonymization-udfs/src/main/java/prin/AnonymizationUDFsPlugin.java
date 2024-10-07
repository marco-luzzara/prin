package prin;

import java.util.HashSet;
import java.util.Set;

import io.trino.spi.Plugin;
import prin.udfs.ShowFirstAndLastChar;

public class AnonymizationUDFsPlugin implements Plugin {
    @Override
    public Set<Class<?>> getFunctions() {
        return Set.of(
                ShowFirstAndLastChar.class);
    }
}