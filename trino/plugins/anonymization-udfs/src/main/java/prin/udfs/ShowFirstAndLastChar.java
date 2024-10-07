package prin.udfs;

import io.airlift.slice.Slice;
import io.airlift.slice.Slices;

import io.trino.spi.function.ScalarFunction;
import io.trino.spi.function.Description;
import io.trino.spi.function.SqlType;
import io.trino.spi.function.SqlNullable;
import io.trino.spi.type.StandardTypes;

public class ShowFirstAndLastChar {
    @ScalarFunction(value = "show_first_and_last", deterministic = true)
    @Description("Show only the first and the last characters of input, the others are hidden by '*'")
    @SqlType(StandardTypes.VARCHAR)
    public static Slice showFirstAndLastChar(
            @SqlNullable @SqlType(StandardTypes.VARCHAR) Slice input) {
        if (input == null || input.length() <= 2)
            return input;

        String inputStr = input.toStringUtf8();

        var anonymizedStr = inputStr.charAt(0) + "*".repeat(inputStr.length() - 2)
                + inputStr.charAt(inputStr.length() - 1);

        return Slices.utf8Slice(anonymizedStr);
    }
}