import scala.math.exp

object ExpDecay {
  val x: Double = 0.5
  val lambda: Double = 1.0
  val maxiter: Int = 1000000

  def main(args: Array[String]): Unit = {
    timeit("expdecay", expdecay())
    timeit("expdecayy", expdecayy())
    timeit("time_expdecay2", time_expdecay2())
  }

  def timeit(name: String, fun: => Any) = {
    def fixlen(s: String, maxlen: Int=16): String = {
      if (s.length > maxlen)
        s.slice(0, maxlen-3) + "..."
      else
        s + " " * (maxlen-s.length)
    }
    val start = System.nanoTime
    fun
    val end = System.nanoTime
    val ns = (end - start) / maxiter
    val us = ns / 1000.0

    val lang = fixlen("Scala")
    val func = fixlen(name)
    val mtps = 1.0 / us
    println(f"$lang%s\t$func%s\t$mtps%.1f mtps\t$us%.3f us/txn")
  }

  def expdecay(x: Double=this.x, lambda: Double=this.lambda): Double = {
    var i: Int = 0
    var y: Double = 0.0
    for (i <- 0 until maxiter) {
      y = exp(-lambda * x)
    }
    y
  }

  def expdecayy(x: Double=this.x, lambda: Double=this.lambda): Double = {
    var i: Int = 0
    var y: Double = 0.0
    0 until maxiter foreach { _ => y = exp(-lambda * x) }
    y
  }

  def expdecay2(x: Double=this.x, lambda: Double=this.lambda): Double = {
    val y: Double = exp(-lambda * x)
    y
  }

  def time_expdecay2(x: Double=this.x, lambda: Double=this.lambda): Double = {
    var y: Double = 0
    0 until maxiter foreach { _ => y = expdecay2()}
    y
  }
}
