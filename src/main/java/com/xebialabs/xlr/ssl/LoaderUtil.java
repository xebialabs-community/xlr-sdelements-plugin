package com.xebialabs.xlr.ssl;

import java.net.URL;

public class LoaderUtil {
    private static ClassLoader getClassLoaderOfClass(final Class<?> clazz) {
        ClassLoader cl = clazz.getClassLoader();
        if (cl == null) {
            return ClassLoader.getSystemClassLoader();
        } else {
            return cl;
        }
    }

    private static URL getResource(String resource, ClassLoader classLoader) {
        return classLoader.getResource(resource);
    }

    public static URL getResourceBySelfClassLoader(String resource) {
        return getResource(resource, getClassLoaderOfClass(LoaderUtil.class));
    }

}
