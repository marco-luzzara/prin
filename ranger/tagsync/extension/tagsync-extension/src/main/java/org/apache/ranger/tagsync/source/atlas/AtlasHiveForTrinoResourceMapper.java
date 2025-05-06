package org.apache.ranger.tagsync.source.atlas;

import java.util.Optional;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.apache.ranger.tagsync.source.atlas.AtlasHiveResourceMapper;
import org.apache.ranger.plugin.model.RangerPolicy.RangerPolicyResource;
import org.apache.ranger.plugin.model.RangerServiceResource;
import org.apache.ranger.tagsync.source.atlasrest.RangerAtlasEntity;

public class AtlasHiveForTrinoResourceMapper extends AtlasHiveResourceMapper {
    private static final Logger LOG = LoggerFactory.getLogger(AtlasHiveForTrinoResourceMapper.class);

    public static final String RANGER_TYPE_TRINO_CATALOG = "catalog";
    public static final String RANGER_TYPE_TRINO_SCHEMA = "schema";

    // TODO: constructor?

    @Override
	public RangerServiceResource buildResource(final RangerAtlasEntity entity) throws Exception {
        final String trinoServiceName = Optional.ofNullable(System.getenv("TRINO_SERVICE_NAME")).orElse("dev_trino");
        final String trinoCatalogName = Optional.ofNullable(System.getenv("TRINO_CATALOG_NAME")).orElse("hive");
        final String trinoSchemaName = Optional.ofNullable(System.getenv("TRINO_SCHEMA_NAME")).orElse("default");

        RangerServiceResource hiveResource = super.buildResource(entity);
        LOG.info("Applying resource policy tranformation to " + hiveResource);

        hiveResource.setServiceName(trinoServiceName);
        Map<String, RangerPolicyResource> resourceElements = hiveResource.getResourceElements();

        // add catalog resource policy
        resourceElements.put(RANGER_TYPE_TRINO_CATALOG, new RangerPolicyResource(trinoCatalogName));

        // remove database policy and add schema resource policy
        RangerPolicyResource policyResourceForDb = resourceElements.get(AtlasHiveResourceMapper.RANGER_TYPE_HIVE_DB);
        resourceElements.remove(AtlasHiveResourceMapper.RANGER_TYPE_HIVE_DB);
        resourceElements.put(RANGER_TYPE_TRINO_SCHEMA, policyResourceForDb);

        LOG.info("Transformed policy resource: " + hiveResource);

        return hiveResource;
    }
}