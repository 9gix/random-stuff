object Timer
{
    def rpm(callback: () => Unit): Unit =
    {
        while (true)
        {
            callback()
            Thread.sleep(1000)
        }
    }
    
    def main(args: Array[String]): Unit =
    {
        rpm(()=>Console.println("Hello World"))
    }
}
