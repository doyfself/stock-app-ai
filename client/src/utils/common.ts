/**
 * 防抖函数 (Debounce)
 * 多次触发时，只在最后一次触发后延迟执行
 * @param func 待执行函数
 * @param wait 延迟时间(毫秒)
 * @param immediate 是否立即执行（首次触发时立即执行，之后延迟）
 * @returns 包装后的函数
 */
export function debounce<F extends (...args: Parameters<F>) => ReturnType<F>>(
  func: F,
  wait: number,
  immediate = false
): (...args: Parameters<F>) => void {
  let timeout: NodeJS.Timeout | null = null;

  return function (this: ThisParameterType<F>, ...args: Parameters<F>): void {

    // 清除已有定时器
    if (timeout) {
      clearTimeout(timeout);
    }

    if (immediate) {
      // 立即执行模式
      const shouldExecute = !timeout;
      // 重置定时器，确保wait时间内再次触发不会重复执行
      timeout = setTimeout(() => {
        timeout = null;
      }, wait);
      // 首次触发时执行
      if (shouldExecute) {
        func.apply(this, args);
      }
    } else {
      // 延迟执行模式
      timeout = setTimeout(() => {
        func.apply(this, args);
        timeout = null;
      }, wait);
    }
  };
}

/**
 * 节流函数 (Throttle)
 * 规定时间内只执行一次
 * @param func 待执行函数
 * @param wait 间隔时间(毫秒)
 * @param trailing 是否在最后一次触发后补执行
 * @returns 包装后的函数
 */
export function throttle<F extends (...args: Parameters<F>) => ReturnType<F>>(
  func: F,
  wait: number,
  trailing = false
): (...args: Parameters<F>) => void {
  let timeout: NodeJS.Timeout | null = null;
  let lastExecuteTime = 0;

  return function (this: ThisParameterType<F>, ...args: Parameters<F>): void {
    const now = Date.now();
    const elapsed = now - lastExecuteTime;

    // 清除延迟执行的定时器
    if (timeout) {
      clearTimeout(timeout);
      timeout = null;
    }

    // 如果距离上次执行时间超过等待时间，立即执行
    if (elapsed >= wait) {
      func.apply(this, args);
      lastExecuteTime = now;
    } else if (trailing) {
      // 否则设置延迟执行（补执行最后一次）
      timeout = setTimeout(() => {
        func.apply(this, args);
        lastExecuteTime = Date.now();
        timeout = null;
      }, wait - elapsed);
    }
  };
}
