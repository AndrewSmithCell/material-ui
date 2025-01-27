import excludeVariablesFromRoot from './excludeVariablesFromRoot';

export default <
    T extends {
      colorSchemeSelector?: 'media' | 'class' | 'data' | string;
      colorSchemes?: Record<string, any>;
      defaultColorScheme?: string;
      cssVarPrefix?: string;
    },
  >(
    theme: T,
  ) =>
  (colorScheme: keyof T['colorSchemes'] | undefined, css: Record<string, any>) => {
    const selector = theme.colorSchemeSelector;
    let rule = selector;
    if (selector === 'class') {
      rule = '.%s';
    }
    if (selector === 'data') {
      rule = '[data-%s]';
    }
    if (selector?.startsWith('data-') && !selector.includes('%s')) {
      // 'data-mui-color-scheme' -> '[data-mui-color-scheme="%s"]'
      rule = `[${selector}="%s"]`;
    }
    if (theme.defaultColorScheme === colorScheme) {
      if (colorScheme === 'dark') {
        const excludedVariables: typeof css = {};
        excludeVariablesFromRoot(theme.cssVarPrefix).forEach((cssVar) => {
          excludedVariables[cssVar] = css[cssVar];
          delete css[cssVar];
        });
        if (rule === 'media') {
          return {
            ':root': css,
            '@media (prefers-color-scheme: dark) { :root': excludedVariables,
          };
        }
        if (rule) {
          return {
            [rule.replace('%s', colorScheme)]: excludedVariables,
            ':root': css,
          };
        }
        return { ':root': { ...css, ...excludedVariables } };
      }
    } else if (colorScheme) {
      if (rule === 'media') {
        return `@media (prefers-color-scheme: ${String(colorScheme)}) { :root`;
      }
      if (rule) {
        return rule.replace('%s', String(colorScheme));
      }
    }
    return ':root';
  };
