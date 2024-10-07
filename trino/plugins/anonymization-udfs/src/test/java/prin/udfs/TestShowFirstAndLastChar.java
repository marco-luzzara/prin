package prin.udfs;

import prin.AnonymizationUDFsPlugin;
import prin.udfs.ShowFirstAndLastChar;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import io.trino.Session;
import io.trino.testing.StandaloneQueryRunner;
import io.trino.testing.QueryRunner;
import io.trino.testing.AbstractTestQueryFramework;

import static io.trino.plugin.tpch.TpchMetadata.TINY_SCHEMA_NAME;
import static io.trino.testing.TestingSession.testSessionBuilder;

import java.util.Optional;

final class TestShowFirstAndLastChar extends AbstractTestQueryFramework {
    private final ShowFirstAndLastChar udf = new ShowFirstAndLastChar();

    @Override
    protected QueryRunner createQueryRunner() {
        Session defaultSession = testSessionBuilder()
                .setCatalog("local")
                .setSchema(TINY_SCHEMA_NAME)
                .build();

        QueryRunner queryRunner = new StandaloneQueryRunner(defaultSession);
        queryRunner.installPlugin(new AnonymizationUDFsPlugin());

        return queryRunner;
    }

    void testShowFirstAndLastChar_whenInputNull_thenReturnNull() {
        assertQuery("SELECT show_first_and_last(NULL)", "SELECT NULL");
    }

    @ParameterizedTest
    @CsvSource(delimiter = '|', quoteCharacter = '"', textBlock = """
            #-----------------------------
            #   Input       |     Anonymized
            #-----------------------------
                ""          |   ""
            #-----------------------------
                a           |   a
            #-----------------------------
                ab          |   ab
            #-----------------------------
                abc         |   a*c
            #-----------------------------
                abcd        |   a**d
            #-----------------------------
            """)
    void testShowFirstAndLastChar_parameterized(String input, String anonymized) {
        assertQuery(String.format("SELECT show_first_and_last('%s')", input),
                String.format("SELECT '%s'", anonymized));
    }
}
