object Timer
{
    def rpm(seconds: Int, callback: () => Unit): Unit =
    {
        while (true)
        {
            callback()
            Thread.sleep(seconds * 1000)
        }
    }
 
    def main(args: Array[String]): Unit =
    {
        rpm(2, ()=>Console.println("Hello World"))
    }
}
